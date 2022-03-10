import math
import random

from player.Opponent import *
from player.RandomAI import *

class SearchAI(RandomAI):
    """
    An AI that makes moves based on a heuristic.
    This is based on the minimax algorithm to select the best move
    """

    def search(self, target_opponent):
        current_hand = self.hand
        best_card = self.evaluate(current_hand, target_opponent)
        return best_card

    def utility(self, asked_card: str, target_opponent: Opponent):
        """ Return the utility of the card if card was found (+1), otherwise return 0 """
        if target_opponent.has_card(asked_card):
            print(f"HAS THE CARD {asked_card}?")
            return target_opponent.hand[asked_card]
        return 0

    def evaluate(self, current_hand, target_opponent: Opponent) -> str:
        # THIS FUNCTION IS INCOMPLETE
        # the weight of cards should be based on whether there is more cards for a certain type
        # all cards regardless of their suit/color have the same value
        utility_hand = current_hand.copy()
        utility_hand = {k: v for k, v in sorted(utility_hand.items(), key=lambda item: item[1])}

        for card, amount in reversed(utility_hand.items()):
            utility_hand[card] += self.utility(card, target_opponent)
        print("after utility")
        print(utility_hand)

        best_val = max(utility_hand.values())
        best_card = max(utility_hand, key=utility_hand.get)
        print(best_card)

        return best_card


    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        best_moves = [] # collect best possible moves from all available opponents
        for opp_name, opp in self.opponents.items():
            best_card = self.search(opp)
            best_moves.append(Move(self.name, opp_name, best_card))

        if len(best_moves) > 0:
            # temporary, will have to find the best with multiple opponents later
            return best_moves[0]

        # perform the search to find the best card to choose for this move
        return super().make_move(other_players, deck_count)

