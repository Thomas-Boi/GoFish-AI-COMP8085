from typing import List
import random

import util


class Deck:
    def __init__(self):	
        """
        A standard 52-cards deck of cards. There are no suits
        since it doesn't matter for Go Fish.
        """
        self.cards = util.create_empty_cards_dict(4)

    def draw(self, amount: int) -> List[str]:
        """
        Draw amount of cards from the deck.
        :return a list of the cards drawn from the deck.
        """
        cards_drawn = []
        for x in range(amount):
            remaining_cards = [card for card in self.cards.keys() if self.cards[card] != 0]
            card = random.choice(remaining_cards)
            cards_drawn.append(card)
            self.cards[card] -= 1

        return cards_drawn
            
    def go_fish(self) -> List[str]:
        return self.draw(1)