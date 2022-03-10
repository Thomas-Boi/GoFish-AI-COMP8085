import colorama


import Game
from player.HumanPlayer import HumanPlayer
from player.RandomAI import RandomAI
from player.OppAwareAI import OppAwareAI
from player.SearchAI import SearchAI

def main():
    colorama.init()
    players_config = {
        # "Random": RandomAI,
        # "You": HumanPlayer,
        "OppAware": OppAwareAI,
        "SearchAI": SearchAI
    }
    result = { key:0 for key in players_config}
    result["Tie"] = 0
    result["Total"] = 0

    # play the game
    for i in range(1):
        players = [constructor(name) for name, constructor in players_config.items()]

        game = Game.Game(players)
        game.play()
        result["Total"] += 1

        if len(game.winners) > 1:
            result["Tie"] += 1
        else:
            result[game.winners[0].name] += 1 

    print("\nRESULT")
    print(result)

if __name__ == "__main__":
    # use a main method wrapper so we can use function
    # hoisting
    main()