from colorama import Fore
import random
from typing import List, Union
import time

from util import color_text
from Deck import Deck
from player.Player import Player
from Move import Move


class Game:
    def __init__(self, players: List[Player]) -> None:
        """
        Represents a GoFish game. This game follows the standard
        Go Fish rules laid out here: https://www.officialgamerules.org/go-fish
        :param a list of players that will be playing the game.
        """
        if len(players) < 2:
            raise ValueError("Requires at least 2 players to play Go Fish.")

        self.deck = Deck()
        """
        The deck.
        """

        self.players = players
        """
        The players in the game.
        """

        self.cur_index = 0
        """
        The index of the player who's making a move.
        """

        self.winners = []
        """
        Track the winners in the game.
        """

        self.__init_game()

    def __init_game(self):
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

        for player in self.players:
            # update the players on the state of the board starting out
            opps = self.get_stats_from_opponents(player)
            player.set_initial_state(opps, len(self.deck.cards))

        # shuffle the cur_index so player who goes first
        # start randomly each round
        self.cur_index = random.randint(0, len(self.players) - 1)

    def play(self, verbose=True, slow=True, human_mode=False):
        """
        Play the game.
        :param verbose, whether to print out extra info in the game.
        :param slow, whether to wait after a move for the user to catch up with the game.
        :param human_mode, whether to print out the hand of non-human opponents.
        """
        if verbose:
            print(color_text("Starting The Game...", Fore.YELLOW))

        
        # before we start, check if anyone got 4 of a kind
        for player in self.players:
            player_hand = player.hand
            has_four = False
            for card in player_hand:
                has_four = player.check_for_fours_in_hand(card)

            if has_four:
                print(f"{color_text('LUCKY', Fore.YELLOW)}! Player {color_text(player.name, Fore.CYAN)} found a four-of-a-kind at the start!")
                
        while not self.is_game_ended():
            cur_player = self.players[self.cur_index]
            if verbose:
                print("-------")
                print(f"It's {color_text(cur_player.name, Fore.CYAN)}'s turn.")

                if human_mode:
                    # only print if it's our hand
                    if cur_player.__class__.__name__ == "HumanPlayer":
                        print(cur_player.get_hands_detailed())
                else:
                    # else, just print out so we can track what the AI has
                    print(cur_player.get_hands_detailed())

                fours = None
                if len(cur_player.fours) > 0:
                    fours = ", ".join(cur_player.fours)
                print(f"{color_text(cur_player.name, Fore.CYAN)}'s fours-of-a-kinds are: {color_text(fours, Fore.GREEN)}.")

                # humans don't need to know this
                if not human_mode:
                    opps = [f"  -{str(opp)}" for opp in cur_player.opponents.values()]
                    formatted_opps = '\n'.join(opps)
                    print(f"Knowledge about opponents: \n{(formatted_opps)}")
                    print("\n")

            # cur player will decide who to ask and what to ask for
            other_players = self.get_stats_from_opponents(self.players[self.cur_index])

            # check to ensure players picked the right card and target
            cur_player.update_opponents(other_players)
            move = cur_player.make_move(other_players, len(self.deck.cards))
            if not cur_player.has_card(move.card):
                print(f"Invalid choice! {color_text(move.asker, Fore.RED)} must ask for a card in their own hand.")
                continue

            # get the target player and ask them
            target = self.get_player_by_name(move.target)
            if target is None:
                print(f"Invalid target name {color_text(move.target, Fore.RED)}! Must choose a player within the game.")
                continue

            if target.has_card(move.card):
                # get a card
                amount = target.get_cards(move.card)
                cur_player.give_cards(move.card, amount)
                if cur_player.check_for_fours_in_hand(move.card):
                    move.found_fours = move.card
                    move.fours_source = Move.ASKING
                move.ask_succeed = True
                move.amount = amount
            else:
                # GO FISH
                fish = self.deck.go_fish()
                cur_player.give_cards(fish)
                if fish == move.card:
                    move.fish_succeed = True

                if cur_player.check_for_fours_in_hand(fish):
                    move.found_fours = fish
                    move.fours_source = Move.FISHING

            if verbose:
                print(move, end='\n\n')
                if slow: time.sleep(2)

            # update all the players on result of move
            for player in self.players:
                player.update_player_state(move)

            # if the player got the card they wanted, they can go again
            # else, turn pass to next player
            if not (move.fish_succeed or move.ask_succeed):
                self.cur_index = (self.cur_index + 1) % len(self.players)

        # loop ended => see who's the winner        
        condition = "A player emptied their hands!"
        if len(self.deck.cards) == 0:
            condition = "The deck is emptied!"
        if verbose:
            print(f"{color_text('GAME ENDED', Fore.YELLOW)}: {color_text(condition, Fore.YELLOW)} Finding the winner...")

        winners = []
        winnerAmount = -1
        for player in self.players:
            amount = len(player.fours)
            if amount > winnerAmount:
                winners = [player]
                winnerAmount = amount
            elif amount == winnerAmount:
                winners.append(player)

        if verbose:
            if len(winners) == 1:
                print(f"Congratulations! {color_text(winners[0].name, Fore.CYAN)} is the winner!")
            elif len(winners) > 1:
                print(
                    f"IT'S A TIE! Victory is shared between {color_text(', '.join([winner.name for winner in winners]), Fore.CYAN)}.")
            else:
                # this shouldn't happen
                print(f"NO WINNER!")
        
        self.winners = winners

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

    def get_stats_from_opponents(self, player: Player):
        """
        Get the stats of the player's opponents.
        :param player the player.
        """
        opps = []
        for a_player in self.players:
            # skip the own player
            if player.name == a_player.name:
                continue
            opps.append(a_player.get_stats_as_seen_from_opp())
        return tuple(opps)

    def get_player_by_name(self, name: str) -> Union[Player, None]:
        """
        Get the player by name. If there's None matching that name, returns
        None.
        """
        for player in self.players:
            if player.name == name:
                return player
