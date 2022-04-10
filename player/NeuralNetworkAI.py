import torch.nn as nn
import torch
from util import device
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
        # layers
        # first is a tanh
        self.tanh = nn.Tanh().to(device)
        # then a linear layer that narrows down to 13
        self.m1 = nn.Linear(input_size, output_size).to(device)
        self.softmax = nn.LogSoftmax(dim=0).to(device)

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
        # for tensor in tensors:
        #     print(tensor.shape)
        concated_input = torch.cat(tensors)
        # print(concated_input.shape)

        result = self.tanh(concated_input)
        output = self.m1(result)
        return self.softmax(output) # softmax before we return

    def train(self, X, Y, model, learning_rate, loss_fn, optimizer=None):
        y_pred = model(X)
        loss = loss_fn(y_pred, y)

        if optimizer:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        else:
            model.zero_grad()
            with torch.no_grad():
                for param in model.parameters():
                    param -= learning_rate * param.grad

        return loss