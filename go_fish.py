import colorama
from argparse import ArgumentParser


import Game
from player.HumanPlayer import HumanPlayer
from player.RandomAI import RandomAI
from player.OppAwareAI import OppAwareAI
from player.SearchAI import SearchAI

def ai_play():
    """
    Create play sessions intended for AI development and training.
    """
    colorama.init()
    players_config = {
        # "Random": RandomAI,
        # "Random1": RandomAI,
        # "Random2": RandomAI,
        # "You": HumanPlayer,
        "OppAware1": OppAwareAI,
        "OppAware2": OppAwareAI,
        "OppAware3": OppAwareAI,
        # "OppAware4": OppAwareAI,
        "SearchAI": SearchAI
    }
    result = { key:0 for key in players_config}
    result["Tie"] = 0
    result["Total"] = 0

    # play the game
    for i in range(100):
        players = [constructor(name) for name, constructor in players_config.items()]

        game = Game.Game(players)
        game.play(False, slow=False)
        result["Total"] += 1

        if len(game.winners) > 1:
            result["Tie"] += 1
        else:
            result[game.winners[0].name] += 1 

    print("\nRESULT")
    print(result)
    
    print("\nRESULT PERCENTAGE")
    percentage = {key: "{:.2f}%".format(val / result["Total"] * 100) for key, val in result.items()}
    print(percentage)

def human_play():
    """
    Create a Go Fish game where a human player plays against
    1-3 bot players.
    """
    colorama.init()
    players_config = {
        # "Random": RandomAI,
        # "Random1": RandomAI,
        # "Random2": RandomAI,
        "You": HumanPlayer,
        "OppAware1": OppAwareAI,
        "OppAware2": OppAwareAI,
        "OppAware3": OppAwareAI
    }
    players = [constructor(name) for name, constructor in players_config.items()]

    game = Game.Game(players)
    game.play(True, True, True)

if __name__ == "__main__":
    # use a main method wrapper so we can use function
    # hoisting
    # ai_play()
    human_play()