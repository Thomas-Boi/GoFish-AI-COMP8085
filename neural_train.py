import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import torch.nn as nn
import torch

from player.NeuralNetworkAI import NeuralNetworkAI


if __name__ == "__main__":

    INPUT_SIZE = 55
    OUTPUT_SIZE = 13
    model = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)

    df = pd.read_csv("rounds_data.csv")
    df.drop("successful_ask", axis=1, inplace=True)

    #pd.set_option('display.max_columns', None)
    duplicate = df[df.duplicated()]
    df = df.drop_duplicates()

    loss_fn = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
