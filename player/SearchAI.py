import math

from player.Opponent import *
from player.RandomAI import *

infinity = math.inf

class SearchAI(RandomAI):
    """
    An AI that makes moves based on a heuristic.
    Uses the Minimax algorithm to select the best move
    """
    def minimax(self, target_opponent) -> Move:
        max_depth = 2
        current_depth = 0
        chosen_card, best_value = self.max_value(target_opponent, current_depth, max_depth)
        return Move(self.name, target_opponent.name, chosen_card)

    def max_value(self, target_opponent, current_depth: int, max_depth: int) -> [str, float]:

        best_card = None
        best_value = -infinity

        # temporarily added
        cards = []
        for card, amount in self.hand.items():
            for i in range(amount):
                cards.append(card)
        return random.choice(cards), best_value

    def min_value(self, target_opponent, current_depth: int, max_depth: int) -> [str, float]:

        best_card = None
        best_value = infinity

    def utiliity(self) -> int:
        pass

    def evaluate(self, target_opponent) -> int:
        # the weight of cards should be based on whether there is more cards for a certain type
        # Ex: if current player hand has 2,3,3,4,4,4 => the 4's would have more weight => look to opponent hand

        # all cards regardless of their suit/color have the same value =>
        # its how many of a card out of the total cards a player has affects the value

        return -1

    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        # pick a random player
        target = random.choice(other_players)

        # perform minimax to find the best card to choose for this move
        return self.minimax(target)
