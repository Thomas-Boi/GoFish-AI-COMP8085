from colorama import Fore
from typing import Dict, Set, Tuple
from collections import namedtuple

import util
from Move import Move

VaguePlayerStat = namedtuple("VaguePlayerStat", ['name', 'hand_size', 'fours'])
"""
Stores the stat that this player can see from other players.
"""

class Player:
    """
    An abstract player class that represents human or computer players.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        """
        Name of the player.
        """
        
        self.hand = Player.create_cards_dict()
        """
        The cards in the player's hands.
        """

        self.fours_of_a_kind: Set[str] = set()
        """
        The four of a kinds the player has collected.
        This only stores the value of the four-of-a-kinds.
        Ex: four 2s are stored as one 2 value in the set.
        """


    @staticmethod
    def create_cards_dict(amount=0) -> Dict[str, int]:
        """
        Create an empty dictionary containing the values (2, 3, J, Q, etc.)
        of a card as keys and the amount of it as values.
        :param amount, the default amount of each cards.
        """
        cards = {}
        for i in util.card_values:
            cards[i] = amount

        return cards


    def has_card(self, card) -> bool:
        """
        Check whether the player has the asked card.
        """
        try:
            return self.hand[card] > 0
        except KeyError:
            # invalid key => wrong card name
            return False


    def get_cards(self, card: str) -> int:
        """
        Get all the cards from the player's hand that matches
        the value of `card`. If there's no card, return 0
        :param the card value we are getting from the players.
        :return the amount of cards matching the given card
        in the player's hand.
        """
        amount = self.hand[card]
        self.hand[card] = 0
        return amount


    def get_hand_size(self) -> int:
        """
        Get the size of the player's hand.
        """
        count = 0
        for amount in self.hand.values():
            count += amount
        return count


    def give_cards(self, card: str, amount: int=1):
        """
        Give the cards to the player based on the amount
        given. If the player got a four-of-a-kind, also update
        itself.
        NOTE: No error check here since we assume the deck is 
        fairly constructed aka no more than 4 cards per value.
        :param card
        :param amount, the amount we are giving to the player.
        """
        self.hand[card] += amount


    def check_for_fours_in_hand(self, card: str) -> bool:
        """
        Determines whether the player found a fours-of-a-kind
        for the card in hand. This doesn't check the player's
        fours-of-a-kind that's laid out for everyone to see.
        """
        # got 4 of a kind
        if self.hand[card] == 4:
            self.fours_of_a_kind.add(card)
            self.hand[card] = 0
            return True

        return False
        

    def get_stats_as_seen_from_opp(self):
        """
        Get the stats of the player as seen from the opponent's
        POV. This means they can see the player's name, hand count
        and four-of-a-kinds player already collected.
        """
        return VaguePlayerStat(self.name, self.get_hand_size(), list(self.fours_of_a_kind))

    def get_hands_detailed(self) -> str:
        """
        Get the player's hand in all details. This shows ALL the values so use carefully.
        """
        txt = f"{util.color_text(self.name, Fore.CYAN)}'s hand: "
        cards = []
        for value, amount in self.hand.items():
            if amount == 0:
                continue

            cards.append(f"{Fore.CYAN}{amount}{Fore.WHITE} of {Fore.YELLOW}{value}{Fore.WHITE}s")

        # format it
        txt += ", ".join(cards) + "."
        return txt


    def set_initial_state(self, cards_per_player: int, player_amounts: int, deck_count: int):
        """
        Set the initial state of the player.
        :param cards_per_player, the amount of cards in each player's hands.
        :param player_amounts, the amount of players in the game (including ourselves.).
        :param deck_count, the amount of cards in the deck.
        """
        pass


    def update_player_state(self, move: Move):
        """
        Update the state of the player based on a move.
        """
        pass


    def make_move(self, other_players: Tuple[VaguePlayerStat], deck_count: int) -> Move:
        """
        Make a move and ask a player for a card.
        :return a tuple of target player, which is a number, and a card
        to ask that player.
        """
        raise NotImplementedError()
