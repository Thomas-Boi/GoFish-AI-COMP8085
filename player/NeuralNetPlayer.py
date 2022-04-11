from player.OppAwareAI import *
from player.NeuralNetworkAI import NeuralNetworkAI
from util import device, card_values
import torch
from typing import List, Iterable
from Deck import DECK_SIZE, SUITS

MAX_OPPONENTS = 3
"""
Max amount of opponents the game will have.
"""

AMOUNT_OF_CARD_VALUES = len(card_values)
"""
The amount of each card type in the game (2, 3, 4, J, Q, etc.).
In a standard deck, the value is 13.
"""

CARD_VALUE_TENSOR_INDEX_DICT = {}
"""
Convert the card value into a tensor index from 0-12.
"""
for i in range(len(card_values)):
    CARD_VALUE_TENSOR_INDEX_DICT[card_values[i]] = i


class NeuralNetPlayer(OppAwareAI):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        # initial input size:
        # number of card types in own hand(1x13) 
        # + number of card types from one opponent (1x13)
        # + hand size of each opponent (1x1)
        # + number of card types from other opponents combined (1x13)
        # + hand size of other opponents combined (1x1)
        # + four of a kinds (1x13)
        # + deck size (1x1)
        # = (1X55)
        INPUT_SIZE = 55
        OUTPUT_SIZE = 13
        self.network = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        self_hand_tensor = self.create_self_hand_tensor()
        fours = self.create_fours_tensor(other_players)
        deck_size_tensor = self.create_deck_size(deck_count)

        # loop through each player and focus on them
        best_score = -1
        opp_to_choose = None
        best_card = None
        for opp in other_players:
            # focus on one opp 
            opp_hand_cards = self.create_opp_hand_tensor(opp)
            opp_hand_sizes = self.create_opp_size_tensor(opp)

            # get the stats of the other opponents
            other_opps = [other_opp for other_opp in other_players if other_opp != opp]
            others_hand_cards = self.create_others_hand_tensor(other_opps)
            others_hand_sizes = self.create_others_size_tensor(other_opps)

            # get the possible cards to ask the opponent
            result_tensor = self.network(self_hand_tensor, 
                opp_hand_cards,
                opp_hand_sizes,
                others_hand_cards,
                others_hand_sizes,
                fours,
                deck_size_tensor)

            # get the most likely card 
            highest_card_score = result_tensor.topk(1).values[0]

            # compare it => if it's better, save 
            if highest_card_score > best_score:
                best_score = highest_card_score
                best_card_index = result_tensor.topk(1).indices[0]
                best_card = card_values[best_card_index]
                opp_to_choose = opp.name

        # return the best option if possible, else make a random move
        if best_card is None:
            return self.make_random_move(other_players)
        return Move(self.name, opp_to_choose, best_card)

    def create_self_hand_tensor(self) -> torch.Tensor:
        # convert this hand's card amounts to tensor
        cur_hand = [val / DECK_SIZE for val in self.hand.values()]
        return torch.FloatTensor(cur_hand, device=device)

    def create_opp_hand_tensor(self, opp_stat: OppStat) -> torch.Tensor:
        opp = self.opponents[opp_stat.name]
        
        # normalize the values
        opp_hand = [val / DECK_SIZE for val in opp.hand.values()]
        return torch.FloatTensor(opp_hand, device=device)

    def create_opp_size_tensor(self, opp_stat: OppStat) -> torch.Tensor:
        return torch.FloatTensor([opp_stat.hand_size / DECK_SIZE], device=device)

    def create_others_hand_tensor(self, opp_stats: List[OppStat]) -> torch.Tensor:
        """
        This represents all the other opponents beside the main opponent we are
        focusing on.
        """
        # 1 X 13 vector, default is 0
        tensor = torch.zeros(AMOUNT_OF_CARD_VALUES)
        for stat in opp_stats:
            # add in place
            tensor.add_(self.create_opp_hand_tensor(stat))
        return tensor

    def create_others_size_tensor(self, opp_stats: List[OppStat]) -> torch.Tensor:
        """
        This represents all the other opponents beside the main opponent we are
        focusing on.
        """
        # 1 X 1 vector, default is 0
        tensor = torch.zeros(1)
        for stat in opp_stats:
            # add in place
            tensor.add_(self.create_opp_size_tensor(stat))
        return tensor

    def create_fours_tensor(self, opp_stats: Tuple[OppStat]) -> torch.Tensor:
        # 1 X 13 vector, default is the user's hand
        # contains the amount of cards to make a 4 then divide by 52.
        # e.g [0, 0, 1/13, 0, 1/13] would mean card value 4 and card value 6 have collected
        tensor = torch.FloatTensor(self.create_a_four_tensor(self.fours))
        for stat in opp_stats:
            # add in place
            tensor.add_(self.create_a_four_tensor(stat.fours))
        return tensor

    def create_a_four_tensor(self, fours: Iterable[str]):
        """
        Make a tensor for a four-of-a-kind information.
        """
        # make an empty tensor
        fours_tensor = torch.zeros(AMOUNT_OF_CARD_VALUES, device=device)

        # fill in the spots where we have a four of a kind
        for card in fours:
            i = CARD_VALUE_TENSOR_INDEX_DICT[card]
            fours_tensor[i] = SUITS / DECK_SIZE

        return fours_tensor

    def create_deck_size(self, deck_size: int) -> torch.Tensor:
        # turn the current deck size into tensor
        return torch.FloatTensor([deck_size / DECK_SIZE], device=device)
