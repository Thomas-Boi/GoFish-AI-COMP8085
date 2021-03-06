import torch.nn as nn
import torch
from util import device
from typing import List

class NeuralNetworkAI(nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetworkAI, self).__init__()
        # layers
        # first is a tanh
        self.tanh = nn.Tanh()
        # then a linear layer that narrows down to 13
        self.m1 = nn.Linear(input_size, output_size)
        nn.init.xavier_uniform_(self.m1.weight)

        self.softmax = nn.Softmax(dim=0)

    def forward(self, self_hand_tensor: torch.Tensor, 
        opp_hand_cards: torch.Tensor, 
        opp_hand_sizes: torch.Tensor, 
        others_hand_cards: torch.Tensor, 
        others_hand_sizes: torch.Tensor, 
        fours: torch.Tensor, deck_size_tensor: torch.Tensor) -> torch.Tensor:
        """
        """
        tensors = [self_hand_tensor]
        tensors.append(opp_hand_cards)
        tensors.append(opp_hand_sizes)
        tensors.append(others_hand_cards)
        tensors.append(others_hand_sizes)
        tensors.append(fours)
        tensors.append(deck_size_tensor)

        # recall each we want to make a long tensor of size 1 X inputSize from the input
        # dim = 0 is row, dim = 1 is column
        concated_input = torch.cat(tensors)
        mo1 = self.m1(concated_input)
        output = self.tanh(mo1)
        return self.softmax(output) # softmax before we return
