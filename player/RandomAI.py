import random
from player.Player import *

class RandomAI(Player):
    """
    An AI that makes random moves.
    """
    def make_move(self, other_players: Tuple[VaguePlayerStat], deck_count: int) -> Move:
        # pick a random player 
        target = random.choice(other_players)

        # pick a random card, if there's more of those card, more likely to ask for it
        cards = []
        for card, amount in self.hand.items():
            for i in range(amount):
                cards.append(card)
        return Move(self.name, target.name, random.choice(cards))