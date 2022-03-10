import math
import random

from player.Opponent import *
from player.OppAwareAI import *


class SearchAI(OppAwareAI):
    """
    An AI that makes moves based on a heuristic.
    This is based on the minimax algorithm to select the best move
    """
    def update_player_state(self, move: Move):
        super().update_player_state(move)

    def search(self, target_opponent: Opponent):
        current_hand = self.hand
        best_card, best_val = self.evaluate(current_hand, target_opponent)
        return best_card, best_val

    def utility(self, asked_card: str, card_amount: int, target_opponent: Opponent):
        """ Return the utility as the amount of cards in the opponents hand if it exists in the bots memory. """
        #print(f"Opp hand: {target_opponent.hand}")
        return target_opponent.hand[asked_card]

    def evaluate(self, current_hand, target_opponent: Opponent):
        """ Evaluate using a greedy algorithm to find the best card with the highest utility. """
        # the final weight of cards should be based on whether there is more cards for a certain type
        # all cards regardless of their suit/color have the same value

        # create a copy of the current hand to store the final utility values
        utility_hand = current_hand.copy()

        for card, amount in utility_hand.items():
            util = self.utility(card, amount, target_opponent)
            #print(f"for card {card}:: bot amount - {amount}, utility - {util}")

            # the final utility is bot_amount * util (opp amount)
            utility_hand[card] = amount * util

        card_amounts = utility_hand.values()
        best_util = max(card_amounts)
        best_card = max(utility_hand, key=utility_hand.get) # type: ignore

        # check if there are more than one card that have the same best utility
        '''dupe_max_values = 0
        for k, v in utility_hand.items():
            if v == best_util:
                dupe_max_values += 1

        # return no card (empty string) and utility of zero if there are cards with the same best utility
        if dupe_max_values > 1:
            return "", 0'''

        return best_card, best_util

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        # collect best possible moves from all available opponents first
        best_moves = []
        for opp_name, opp in self.opponents.items():
            best_card, best_val = self.search(opp) # perform search
            best_moves.append([Move(self.name, opp_name, best_card), best_val])

        # compare best moves from all opponents then choose the one with highest utility if available
        best_move = best_moves[0]
        for move in best_moves:
            val = move[1]
            if val > best_move[1]:
                best_move = move
        if best_move[0] == "":


        # if no best move found then return a card that's both in
        # our hand and the opponent's hand.
        return super().make_move(other_players, deck_count)
