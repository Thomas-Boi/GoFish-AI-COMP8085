import torch.nn as nn
import torch
import util
from typing import List

# TODO
# training function (feed data into update loop)
# update loop (play 1 game, get the loss, backpropagate)
# neural net creation function
# tensor maker (convert game input to tensors)
# loss function
# AI class and architecture -> doing

class NeuralNetworkAI(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        # stats
        self.input_size = input_size
        self.output_size = output_size

        # what kind of input do we want?
        # player's hand (exactly what cards we have)
        # cards that the we know the opponent has (for each opponent)
        # 
        
        # layers
        self.m1 = nn.Linear(input_size, output_size)
        self.softmax = nn.LogSoftmax(dim=-1)
    
    def forward(self, self_hand_tensor: torch.Tensor, 
        opp_hand_cards: List[torch.Tensor], 
        opp_hand_sizes: List[torch.Tensor], 
        fours: List[torch.Tensor], deck_size_tensor: torch.Tensor) -> torch.Tensor:
        """
        """
        tensors = [self_hand_tensor]
        tensors.extend(opp_hand_cards)
        tensors.extend(opp_hand_sizes)
        tensors.extend(fours)
        tensors.append(deck_size_tensor)

        # recall each we want to make a long tensor of size 1 X inputSize from the input
        # dim = 0 is row, dim = 1 is column
        # for tensor in tensors:
        #     print(tensor.shape)
        concated_input = torch.cat(tensors, dim=1)
        # print(concated_input.shape)

        output = self.m1(concated_input)
        return self.softmax(output) # softmax before we return
    
    def initHidden(self):
        return torch.zeros(1, self.hidden_size, device=util.device)