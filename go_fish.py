import colorama


import Game
from player.HumanPlayer import HumanPlayer
from player.RandomAI import RandomAI


def main():
    colorama.init()
    # init the players
    players = [
        HumanPlayer("You"),
        RandomAI("a"),
        RandomAI("b")
    ]

    # play the game
    game = Game.Game(players)
    game.play()

if __name__ == "__main__":
    # use a main method wrapper so we can use function
    # hoisting
    main()