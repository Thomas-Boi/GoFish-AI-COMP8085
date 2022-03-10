import math
import random

from typing import Union 
from player.Opponent import *
from player.OppAwareAI import *


class SearchAI(OppAwareAI):
    """
    An AI that makes moves based on a heuristic.
    This is based on the minimax algorithm to select the best move
    """

    def search(self, target_opponent: Opponent):
        current_hand = self.hand
        best_card, best_val = self.evaluate(current_hand, target_opponent)
        return best_card, best_val

    def utility(self, asked_card: str, target_opponent: Opponent):
        """ Return the utility of the card if card was found (+card amount), otherwise return 0 """
        if target_opponent.hand[asked_card] > 0:
            print(f"HAS THE CARD {asked_card}?")
            return target_opponent.hand[asked_card]
        return 0

    def evaluate(self, current_hand, target_opponent: Opponent):
        # THIS FUNCTION IS INCOMPLETE
        # the weight of cards should be based on whether there is more cards for a certain type
        # all cards regardless of their suit/color have the same value
        utility_hand = current_hand.copy()
        utility_hand = {k: v for k, v in sorted(utility_hand.items(), key=lambda item: item[1])}

        for card, amount in utility_hand.items():
            utility_hand[card] += self.utility(card, target_opponent)

        card_amounts = utility_hand.values()
        best_val = max(card_amounts)
        best_card = max(utility_hand, key=utility_hand.get) # type: ignore

        return best_card, best_val

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        # collect best possible moves from all available opponents
        best_moves = []
        for opp_name, opp in self.opponents.items():
            best_card, best_val = self.search(opp) # perform search
            best_moves.append([Move(self.name, opp_name, best_card), best_val])

        # find best move by comparing best_val
        if len(best_moves) > 0:
            # temporary, will have to find the best with multiple opponents later
            return best_moves[0][0]

        # if no best move found then return a card that's both in
        # our hand and the opponent's hand.
        return super().make_move(other_players, deck_count)
