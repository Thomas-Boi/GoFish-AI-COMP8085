import random
from typing import List, Union

from Deck import Deck
from Player import Player

class Game:
    def __init__(self, players: List[Player]=[]) -> None:
        """
        Represents a GoFish game. This game follows the standard
        Go Fish rules laid out here: https://www.officialgamerules.org/go-fish
        """
        self.deck = Deck()
        self.players = players
        self.cur_index = 0
        """
        The index of the player who's making a move.
        """

    def init_game(self):
        """
        Init the game by dealing the cards to each player.
        """
        initial_hands_count = 7
        if len(self.players) >= 4:
            initial_hands_count = 5

        for player in self.players:
            hand = self.deck.draw(initial_hands_count)
            for card in hand:
                player.give_cards(card)

        # shuffle the cur_index so player who goes first
        # start randomly each round
        self.cur_index = random.randint(0, len(self.players))


    def play(self, verbose=True):
        """
        Play the game.
        """
        while not self.is_game_ended():
            cur_player = self.players[self.cur_index]
            if verbose:
                print(f"It's {cur_player.name}'s turn.")
                print(cur_player.get_hands_detailed(), end='\n\n')

            # cur player will decide who to ask and what to ask for
            other_players = []
            for i in len(self.players):
                if i == self.cur_index:
                    continue
                other_players.append(self.players[i].get_stats_as_seen_from_opp())

            move = cur_player.make_move(tuple(other_players), len(self.deck.cards))

            # get the target player and ask them
            target = self.get_player_by_name(move.target)
            if target.has_card(move.card):
                amount = target.get_cards(move.card)
                cur_player.give_cards(move.card, amount)
                move.found_fours = cur_player.check_for_fours_in_hand(move.card)
                move.succeed = True
                move.amount = amount
            else:
                card = self.deck.go_fish()
                cur_player.give_cards(card)
                move.succeed = False

            if verbose:
                print(move, end='\n\n')

            # update all the players on result of move
            for player in self.players:
                player.update_player_state(move)
            
            # turn pass to the next player IF the move was unsuccessful
            # else, the player can continue to go
            if not move.succeed:
                self.cur_index = (self.cur_index + 1) % len(self.players)

        print("GAME ENDED! Find the winner...")
        # loop ended => see who's the winner        
        # in case of a tie
        winners = []
        winnerAmount = -1
        for player in self.players:
            amount = len(player.fours_of_a_kind)
            if amount > winnerAmount:
                winners = [player]
                winnerAmount = amount
            elif amount == winnerAmount:
                winners.append(player)

        if len(winners) == 1:
            print(f"Congratulations! {winners[0].name} is the winner!")
        elif len(winners) > 1:
            print(f"IT'S A TIE! Victory is shared between {', '.join([winner.name for winner in winners])}.")
        else:
            # this shouldn't happen
            print(f"NO WINNER!")
        

    def is_game_ended(self) -> bool:
        """
        Determines whether the game ended.
        Game play continues until a player runs out of cards or the deck is empty
        """
        if len(self.deck.cards) == 0:
            return True

        for player in self.players:
            if player.get_hand_size() == 0:
                return True

        return False


    def get_player_by_name(self, name: str) -> Union[Player, None]:
        """
        Get the player by name. If there's None matching that name, returns
        None.
        """
        for player in self.players:
            if player.name == name:
                return player
	