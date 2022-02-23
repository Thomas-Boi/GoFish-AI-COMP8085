from colorama import Fore
from player.Player import *

class HumanPlayer(Player):
    """
    Represents a human player or just someone that can enter inputs through 
    the command line.
    """
    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        names = []
        # show info to human player
        
        print(f"There are {color_text(deck_count, Fore.CYAN)} cards in the deck.")
        for player in other_players:
            print(f"{color_text(player.name, Fore.CYAN)}'s hand has {color_text(player.hand_size, Fore.CYAN)} cards.")
            fours = None
            if len(player.fours) > 0:
                fours = ", ".join(player.fours)
            print(f"{color_text(player.name, Fore.CYAN)} collected four-of-a-kinds are: {color_text(fours, Fore.GREEN)}.", end='\n\n')
            names.append(player.name)
            

        # ask for target
        # if there's only 1 opponent => don't need to ask for target.
        target = other_players[0].name
        if len(other_players) > 1:
            target = input("Enter the name of the player you want to get a card from: ")

        # ask for card
        card = input(f"Enter the card you want to get from {target}: ")
        print('\n')

        return Move(self.name, target, card.upper()) # upper input to save typing time
