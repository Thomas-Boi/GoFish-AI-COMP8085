from typing import Dict

from RandomAI import *
from Opponent import *

class OppAwareAI(RandomAI):
    """
    Represents an AI that is aware of its opponents.
    Serve as the base class for more complex AI.
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)


    def update_player_state(self, move: Move):
        """
        Update the state of the player based on a move.
        """
        pass


    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        """
        Make a move and ask a player for a card.
        :return a tuple of target player, which is a number, and a card
        to ask that player.
        """
        # start by checking what cards we have in our hand
        for card in self.hands:
            if self.hands[card] > 0:
                # we have this card => find the first player that has this card
                for other_player_name, other_player in self.other_players.items():
                    # since we use a class => we can use the predefined functions like...
                    if other_player.has_card(card):
                        return Move() # fill out the move here
                        
        # for loop is done but didn't see the return => we didn't find a card
        # => default to RandomAI's random move
        super().make_move()
