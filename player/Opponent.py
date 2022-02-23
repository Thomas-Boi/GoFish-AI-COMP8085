from collections import namedtuple


OppStat = namedtuple("OppStat", ['name', 'hand_size', 'fours'])
"""
Stores the stat that a Player can see from their opponents.
"""

class Opponent:
    def __init__(self) -> None:
        """
        Represents an opponent player from the view of a player.
        This means certain data are not visible to the player.
        """
        self.name = ""
        """
        Name of the opp.
        """

        self.hand_size = ""
        """
        The opp's hand size.
        """

        self.fours = ""
        """
        The amount of fours the opp has.
        """

        self.hand = ""
        """
        The cards in the player's hands.
        """

    def update(self, stat: OppStat):
        """
        Update the opponent's stat.
        """
        for attr, value in stat.items():
            setattr(self, attr, value)
