from player.OppAwareAI import *
from player.NeuralNetworkAI import NeuralNetworkAI

import torch

MAX_OPPONENTS = 3
CARD_TYPES = 13

class NeuralNetPlayer(OppAwareAI):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        # initial input size:
        # number of card types (1x13) + number of card types from one opponent (1x13)*3
        # + four of a kinds (1x13)*3 + hand size of each opponent (1x3) + deck size (1x1)
        # = (1x95)
        INPUT_SIZE = 95
        OUTPUT_SIZE = 13
        # HIDDEN_SIZE = ?? # unknown size for now
        # self.network = NeuralNetworkAI(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)

    def update_player_state(self, move: Move):
        return super().update_player_state(move)
        
    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:

        input_result = self.create_input_tensor(other_players, deck_count)

        return super().make_move(other_players, deck_count)

    def create_hand_tensor(self, hand: Dict):
        pass

    def create_input_tensor(self, opp_stats: Tuple[OppStat], deck_size: int) -> torch.Tensor:
        """
        Takes the current state of the game and converts it to a tensor
        """
        # convert this hand's card amounts to tensor
        current_hand_card_amounts = list(self.hand.values())
        cur_hand_tensor = torch.FloatTensor(current_hand_card_amounts)

        # convert the opp hand's card amounts and the sizes
        # maximum of 3 opponents
        # we need to fill the rest with zeroes if there are less than 3 opponents

        opps_tensor = torch.zeros(MAX_OPPONENTS * CARD_TYPES)

        # handle the card amounts
        all_opp_hands = []
        for opp_name, opp in self.opponents.items():
            opp_card_amounts = list(opp.hand.values())

            all_opp_hands.extend(opp_card_amounts)

        opp_hand_tensor = torch.FloatTensor(all_opp_hands)
        # append the number of zeroes according to the missing opponents to a tensor
        # or combine the tensors afterwards then fill

        opp_hand_sizes = torch.zeros(MAX_OPPONENTS)
        for i in range(0, len(opp_stats)):
            opp_hand_sizes[i] = opp_stats[i].hand_size

        # TODO: handle four-of-a-kinds

        # turn the current deck size into tensor
        deck_tensor = torch.FloatTensor(deck_size)

        return cur_hand_tensor



