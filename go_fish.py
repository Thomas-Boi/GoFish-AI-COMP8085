import colorama
from argparse import ArgumentParser


import Game
from player.HumanPlayer import HumanPlayer
from player.RandomAI import RandomAI
from player.OppAwareAI import OppAwareAI
from player.SearchAI import SearchAI
from player.ProbabilityAI import ProbabilityAI
from player.NeuralNetPlayer import NeuralNetPlayer
from player.Player import Player
from typing import List
import time

def ai_play():
    """
    Create play sessions intended for AI development and training.
    """
    players_config = {
        "Random": RandomAI,
        # "Random1": RandomAI,
        # "Random2": RandomAI,
        # "You": HumanPlayer,
        # "OppAware1": OppAwareAI,
        # "OppAware2": OppAwareAI,
        # "OppAware3": OppAwareAI,
        # "OppAware4": OppAwareAI,
        # "SearchAI": SearchAI
        # "You": HumanPlayer,
        "Prob-Bot": ProbabilityAI,
        # "NeuralNet": NeuralNetPlayer
    }
    result = {key: 0 for key in players_config}
    result["Tie"] = 0
    result["Total"] = 0

    # play the game
    start_time = time.time()
    rounds = 100
    for i in range(rounds):
        players = [constructor(name) for name, constructor in players_config.items()]

        game = Game.Game(players)
        game.play(verbose=False, slow=False)
        result["Total"] += 1

        if len(game.winners) > 1:
            result["Tie"] += 1
        else:
            result[game.winners[0].name] += 1 

    end_time = time.time()

    print("\nRESULT")
    print(result)
    
    print("\nRESULT PERCENTAGE")
    percentage = {key: "{:.2f}%".format(val / result["Total"] * 100) for key, val in result.items()}
    print(percentage)

    print("\nTIME")
    print(f"Total: {end_time - start_time}s")
    print(f"Average Per Round: {(end_time - start_time) / rounds}s")

def human_play(opp_amount: int, opp_type: int):
    """
    Create a Go Fish game where a human player plays against
    1-3 bot players.
    :param opp_amount: the amount of opponents the player will have.
    :param opp_type: 1 is for a RandomAI, 2 is for an OppAwareAI,
    3 is for a SearchAI, 4 is for a ProbabilityAI.
    """
    players: List[Player] = [HumanPlayer("You")]
    opponent_types = [
        RandomAI,
        OppAwareAI,
        SearchAI,
        ProbabilityAI,
        NeuralNetPlayer
    ]
    names = ["a", "b", "c", "d", "e"]

    for i in range(opp_amount):
        players.append(opponent_types[opp_type - 1](names[i]))

    game = Game.Game(players)
    game.play(True, True, True)

def neural_net_train():
    """
    Create play sessions intended for AI development and training.
    """
    # player configs
    players_config = {
        "Random": RandomAI,
        # "Random1": RandomAI,
        # "Random2": RandomAI,
        "Bot": NeuralNetPlayer
    }

    # training hyperparameters
    learning_rate = 0.0005
    hidden_layer_size = 128 # this is our memory
    n_iters = 100000 # number of 'epoch' however, since we aren't looping through a dataset, it's called iterations
    # print_every = 5000
    # plot_every = 500

    # result tracking
    result = {key: 0 for key in players_config}
    result["Tie"] = 0
    result["Total"] = 0

    # play the game
    for i in range(100):
        players = [constructor(name) for name, constructor in players_config.items()]

        game = Game.Game(players)
        game.play(False, slow=False)
        result["Total"] += 1

        # two ways to approach this:
        # update the AI after a game and get the successful ask out of all asks at the end (e.g 20 / 40 ask success rate)
        # OR
        # update the AI after every round that it asked a question -> have to modify the play() 

        # both are relatively easy to make. Don't know which one is better

        if len(game.winners) > 1:
            result["Tie"] += 1
        else:
            result[game.winners[0].name] += 1 

    print("\nRESULT")
    print(result)
    
    print("\nRESULT PERCENTAGE")
    percentage = {key: "{:.2f}%".format(val / result["Total"] * 100) for key, val in result.items()}
    print(percentage)


if __name__ == "__main__":
    # use a main method wrapper so we can use function
    # hoisting
    colorama.init()
    argparser = ArgumentParser(description="A Go Fish environment that can be used for a simple game or an AI training environment.")
    
    argparser.add_argument("--play", help="Whether to go into play mode. Default is false (AI mode)",
        action='store_true')

    argparser.add_argument("--amount", help="The amount of enemies the player is playing against. "
                                            "Must be in play mode for this to count. ",
        type=int, choices=range(1, 4), default=1) # only 1-3 opponents

    argparser.add_argument("--type", help="The type of enemy. 1 for RandomAI, 2 for OppAwareAI, "
                                          "3 for SearchAI, 4 for ProbabilityAI, 5 for NeuralNetAI",
        type=int, choices=range(1, 6), default=5) # default is a neural net bot.

    args = argparser.parse_args()

    if args.play:
        human_play(args.amount, args.type)
    else:
        ai_play()
