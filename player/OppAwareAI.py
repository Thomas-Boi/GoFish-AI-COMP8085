from player.RandomAI import *
from player.Opponent import *

class OppAwareAI(RandomAI):
    """
    Represents an AI that is aware of its opponents.
    Serve as the base class for more complex AI.
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

        # only updates if ask was successful, else nothing happens
        elif move.ask_succeed:
            # check who ask for what => if it's us, don't need to update
            # since the Game updates us already and we know our own stats
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card, move.amount)
                
            if move.target != self.name:
                self.opponents[move.target].remove_card(move.card)  

        elif move.fish_succeed:
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card)

        # regardless if ask or fish succeeded, the asker has the card they just
        # asked for.
        # for now, just increment the card count whenever they ask for the card
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
