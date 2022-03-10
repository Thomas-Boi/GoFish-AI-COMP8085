from player.RandomAI import *
from player.Opponent import *

class OppAwareAI(RandomAI):
    """
    Represents an AI that is aware of its opponents.
    This tracks the amount of cards that a player has in their hand.
    This serves as the base class for more complex AI.

    This only tracks the minimum amount of cards that the opponent has.
    This is due to the unknown nature of asking. A player asking for a card
    might have 1-3 cards of those values. However, we don't know the exact number.
    The only time we know the exact number is when they successfully ask for a card
    and the other player gave them those cards. We do not know when a card is gained
    through fishing.
    """
    def update_player_state(self, move: Move):
        """
        Update the state of the player based on a move.
        """
        # check whether the player found a four => if they did, remove all
        # cards from the game with that value.
        if move.found_fours is not None:
            for opp in self.opponents.values():
                opp.remove_card(move.found_fours)
            # don't do anything else afterwards cause there's no need
            # a four of a kind removes all values like that from the game
            return

        # regardless whether the ask was successful, we know that player has at least
        # 1 card of that value. 
        if move.asker != self.name:
            # if the card is not 0 (already counted), do nothing
            # since we can't tell exactly how many cards are in that player's hand
            # and can only track the minimum aka "at least" amount of that value
            # in hand. Thus, if not tracked yet, add 1 to the card counter.
            # Else, we aren't sure.
            if not self.opponents[move.asker].has_card(move.card): 
                self.opponents[move.asker].give_cards(move.card)

        # only updates if ask was successful, else nothing happens
        if move.ask_succeed:
            # check who ask for what => if it's us, don't need to update
            # since the Game updates us already and we know our own stats
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card, move.amount)
                
            if move.target != self.name:
                self.opponents[move.target].remove_card(move.card)  
            return

        # here, we know that the ask didn't succeed

        if move.fish_succeed:
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card)


    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        """
        Make a move and ask a player for a card.
        :return a tuple of target player, which is a number, and a card
        to ask that player.
        """
        # start by checking what cards we have in our hand
        for card in self.hand:
            if self.hand[card] > 0:
                # we have this card => find the first player that has this card
                for opp_name, opp in self.opponents.items():
                    if opp.has_card(card):
                        return Move(self.name, opp_name, card) 
                        
        # for loop is done but didn't see the return => we didn't find a card
        # => default to RandomAI's random move
        return super().make_move(other_players, deck_count)
