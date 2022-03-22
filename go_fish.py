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

def human_play(opp_amount: int, opp_type: int):
    """
    Create a Go Fish game where a human player plays against
    1-3 bot players.
    :param opp_amount: the amount of opponents the player will have.
    :param opp_type: 1 is for a RandomAI, 2 is for an OppAwareAI,
    3 is for a SearchAI.
    """
    players = [HumanPlayer("You")]
    opponent_types = [
        RandomAI,
        OppAwareAI,
        SearchAI
    ]
    names = ["a", "b", "c"]

    for i in range(opp_amount):
        players.append(opponent_types[opp_type - 1](names[i]))

    game = Game.Game(players)
    game.play(True, True, True)

if __name__ == "__main__":
    # use a main method wrapper so we can use function
    # hoisting
    colorama.init()
    argparser = ArgumentParser(description="A Go Fish environment that can be used for a simple game or an AI training environment.")
    
    argparser.add_argument("--play", help="Whether to go into play mode. Default is false (AI mode)",
        action='store_true')

    argparser.add_argument("--amount", help="The amount of enemies the player is playing against. Must be in play mode for this to count. ",
        type=int, choices=range(1, 4)) # only 1-3 opponents

    argparser.add_argument("--type", help="The type of enemy. 1 for RandomAI, 2 for OppAwareAI, 3 for SearchAI.", 
        type=int, choices=range(1, 4), default=2) # default is a medium bot.

    args = argparser.parse_args()

    if args.play:
        human_play(args.amount, args.type)
    else:
        ai_play()