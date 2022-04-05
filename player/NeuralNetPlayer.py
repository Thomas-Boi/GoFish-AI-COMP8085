from player.OppAwareAI import *
from player.NeuralNetworkAI import NeuralNetworkAI

class NeuralNetPlayer(OppAwareAI):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        
    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        return super().make_move(other_players, deck_count)

    def update_player_state(self, move: Move):
        return super().update_player_state(move)

    def create_tensor(self):
        pass  
