from player.OppAwareAI import *
from player.NeuralNetworkAI import NeuralNetworkAI
from util import device, card_values
import torch
from typing import List, Iterable

MAX_OPPONENTS = 3
"""
Max amount of opponents the game will have.
"""

AMOUNT_OF_CARD_VALUES = len(card_values)
"""
The amount of each card type in the game (2, 3, 4, J, Q, etc.).
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
        # + number of card types from one opponent (1x13)*3
        # + hand size of each opponent (1x1) * 3
        # + four of a kinds (1x13) * 4 
        # + deck size (1x1)
        # = (1x108)
        INPUT_SIZE = 108
        OUTPUT_SIZE = 13
        self.network = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:

        # input_result = self.create_input_tensor(other_players, deck_count)
        self_hand_tensor = self.create_self_hand_tensor()
        opp_hand_cards = self.create_opp_hand_tensor(other_players)
        opp_hand_sizes = self.create_opp_size_tensor(other_players)
        fours = self.create_fours_tensor(other_players)
        deck_size_tensor = self.create_deck_size(deck_count)

        # get the possible cards to ask the opponent
        result_tensor = self.network(self_hand_tensor, 
            opp_hand_cards,
            opp_hand_sizes,
            fours,
            deck_size_tensor)

        # get the most likely card 
        most_likely_card_index = result_tensor.topk(1).indices[0]
        card = card_values[most_likely_card_index]

        # for now, just return the first opponent
        # TODO: return a card and an opponent from the AI
        return Move(self.name, other_players[0].name, card)

    def create_self_hand_tensor(self) -> torch.Tensor:
        # convert this hand's card amounts to tensor
        current_hand_card_amounts = list(self.hand.values())
        return torch.FloatTensor([current_hand_card_amounts], device=device)

    def create_opp_hand_tensor(self, opp_stats: Tuple[OppStat]) -> List[torch.Tensor]:
        # loop through opp stats so we have the same ordering everytime
        # loop through dictionary doesn't preserve the order => risky
        tensors = []
        for stat in opp_stats:
            opp = self.opponents[stat.name]
            opp_hand = list(opp.hand.values())
            tensors.append(torch.FloatTensor([opp_hand], device=device))

        for i in range(MAX_OPPONENTS - len(opp_stats)):
            tensors.append(torch.zeros(1, 13, device=device))

        return tensors

    def create_opp_size_tensor(self, opp_stats: Tuple[OppStat]) -> List[torch.Tensor]:
        tensors = []
        for stat in opp_stats:
            tensors.append(torch.FloatTensor([[stat.hand_size]], device=device))
        
        for i in range(MAX_OPPONENTS - len(opp_stats)):
            tensors.append(torch.zeros(1, 1, device=device))

        return tensors

    def create_fours_tensor(self, opp_stats: Tuple[OppStat]) -> List[torch.Tensor]:
        # the bot's hand will always be first
        tensors = [self.create_a_four_tensor(self.fours)]

        for stat in opp_stats:
            fours = self.create_a_four_tensor(stat.fours)
            tensors.append(fours)
        
        for i in range(MAX_OPPONENTS - len(opp_stats)):
            tensors.append(torch.zeros(1, AMOUNT_OF_CARD_VALUES, device=device))

        return tensors

    def create_a_four_tensor(self, fours: Iterable[str]):
        """
        Make a tensor for a four-of-a-kind information.
        """
        # make an empty tensor
        fours_tensor = torch.zeros(1, AMOUNT_OF_CARD_VALUES, device=device)

        # fill in the spots where we have a four of a kind
        for card in fours:
            i = CARD_VALUE_TENSOR_INDEX_DICT[card]
            fours_tensor[i] = 1

        return fours_tensor

    def create_deck_size(self, deck_size: int) -> torch.Tensor:
        # turn the current deck size into tensor
        return torch.FloatTensor([[deck_size]], device=device)
