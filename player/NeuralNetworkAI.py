import torch.nn as nn
import torch
# TODO
# training function (feed data into update loop)
# update loop (play 1 game, get the loss, backpropagate)
# neural net creation function
# tensor maker (convert game input to tensors)
# loss function
# AI class and architecture -> doing

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class NeuralNetworkAI(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # stats
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # what kind of input do we want?
        # player's hand (exactly what cards we have)
        # cards that the we know the opponent has (for each opponent)
        # 
        
        # layers
        # for m1 and m2, input size the concatenation of input and hidden sizes
        self.m1 = nn.Linear(input_size + hidden_size, output_size)
        self.m2 = nn.Linear(input_size + hidden_size, hidden_size)
        # for m3, input size is the conatenation of the output of m1 and m2
        self.m3 = nn.Linear(output_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=-1)
    
    def forward(self, language, current_letter, hidden_vector):
        """
        :param language, a tensor of size 1 X 18
        :param current_letter, a tensor of size 1 X 59
        :param hidden_vector, a tensor of size 1 X 128
        """
        # recall each we want to make a long tensor of size 1 X 205 from the input
        # dim = 0 is row, dim = 1 is column
        concated_input = torch.cat((language, current_letter, hidden_vector), dim=1)
        
        # print(f"concat_input shape {concated_input.shape}")
        mo1 = self.m1(concated_input)
        mo2 = self.m2(concated_input)
        
        concated_mo = torch.cat((mo1, mo2), dim=1)
        mo3 = self.m3(concated_mo)
        res = self.softmax(mo3)
        return res, mo2
    
    def initHidden(self):
        return torch.zeros(1, self.hidden_size, device=device)