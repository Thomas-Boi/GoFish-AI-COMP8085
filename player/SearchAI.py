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
        return self.evaluate(target_opponent)

    def utility(self, asked_card: str, target_opponent: Opponent):
        """ Return the utility as the amount of cards in the opponents hand if it exists in the bots memory. """
        #print(f"Opp hand: {target_opponent.hand}")
        return target_opponent.hand[asked_card]

    def evaluate(self, target_opponent: Opponent):
        """ Evaluate using a greedy algorithm to find the best card with the highest utility. """
        # the final weight of cards should be based on whether there is more cards for a certain type
        # all cards regardless of their suit/color have the same value

        # create a copy of the current hand to store the final utility values
        utility_hand = {}

        for card, amount in self.hand.items():
            if amount == 0: continue

            util = self.utility(card, target_opponent)

            # the final utility is bot_amount * util (opp amount)
            utility_hand[card] = amount * util

        # check if there are more than one card that have the same best utility
        best_cards = []
        best_util = 0
        for card, util in utility_hand.items():
            if util > best_util:
                best_cards = [card]
                best_util = util
            elif util == best_util:
                best_cards.append(card)

        return random.choice(best_cards), best_util

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        # collect best possible moves from all available opponents first
        potential_best_moves = []
        for opp_name, opp in self.opponents.items():
            best_card, best_util = self.search(opp) # perform search
            potential_best_moves.append([Move(self.name, opp_name, best_card), best_util])

        # compare best moves from all opponents then choose the one with highest utility if available
        best_moves = []
        best_util = 0
        for move, util in potential_best_moves:
            if util > best_util:
                best_moves = [move]
                best_util = util
            elif util == best_util:
                best_moves.append(move)

        # guarantees we always have a choice cause a random
        # move is value 0 => which we always have
        return random.choice(best_moves)
