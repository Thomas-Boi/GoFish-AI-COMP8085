import math
import pandas as pd
import torch.nn as nn
import torch

from typing import List, Iterable

from Deck import SUITS
from util import device
from player.NeuralNetworkAI import NeuralNetworkAI
from player.NeuralNetPlayer import DECK_SIZE, AMOUNT_OF_CARD_VALUES, CARD_VALUE_TENSOR_INDEX_DICT

INPUT_SIZE = 55
OUTPUT_SIZE = 13

def train(self_hand_tensor: torch.Tensor,
          opp_hand_cards: torch.Tensor,
          opp_hand_sizes: torch.Tensor,
          others_hand_cards: torch.Tensor,
          others_hand_sizes: torch.Tensor,
          fours: torch.Tensor,
          deck_size_tensor: torch.Tensor,
          asked_card: torch.Tensor,
          model, learning_rate, loss_fn, optimizer=None):
    """ Train the model for one iteration """

    y_pred = model(self_hand_tensor, opp_hand_cards, opp_hand_sizes,
                   others_hand_cards, others_hand_sizes, fours, deck_size_tensor)
    loss = loss_fn(y_pred, asked_card)

    if optimizer:
        # backpropogate with optimizer
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    else:
        # without optimizer we tune the parameters manually with the passed learning rate
        model.zero_grad()
        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate * param.grad

    return loss


def start_train_session(dataframe, model, loss_fn, optimizer, learning_rate=0.05,
                        epoch=500, decay_rate=0.5, decay_time=50):
    """ Start a training session using the hyperparameters passed to the model """
    last_loss = 0
    losses = []
    for i in range(1, epoch + 1):
        print(f"Epoch {i}")

        for index, row in dataframe.iterrows():
            # convert all features to tensors before feeding to model
            our_hand_tensor = create_self_hand_tensor(row["our_hand"])
            fours_tensor = create_fours_tensor(row["our_fours"],
                                               [row["opp_0_fours"], row["opp_1_fours"], row["opp_2_fours"]])
            deck_size_tensor = create_deck_size(row["deck_size"])

            opp_hand_cards_tensor = create_opp_hand_tensor(row["opp_0_cards"])
            opp_hand_size_tensor = create_opp_size_tensor(row["opp_0_hand_size"])

            others_hand_cards_tensor = create_other_opp_hand_tensor([row["opp_1_cards"], row["opp_2_cards"]])
            others_hand_size_tensor = create_other_opp_size_tensor([row["opp_1_hand_size"], row["opp_2_hand_size"]])

            asked_card_output_tensor = create_asked_card_tensor(row["card_ask"])

            last_loss = train(our_hand_tensor, opp_hand_cards_tensor, opp_hand_size_tensor,
                              others_hand_cards_tensor, others_hand_size_tensor,
                              fours_tensor, deck_size_tensor,
                              asked_card_output_tensor,
                              model, learning_rate, loss_fn,
                              optimizer=optimizer)

            if index % 100000 == 0:
                # get losses for plotting later
                losses.append(last_loss.item())
                print(f"{index}: {last_loss.item()}")

        # stop early if we have low loss or if the loss exploded
        if last_loss <= 0.01:
            print("Loss below 0.01. Ending early.")
            break
        elif last_loss == math.inf or last_loss == -math.inf or last_loss == torch.nan:
            print(f"Loss exploded, value is {last_loss}. Ending early.")
            break

        # decay the learning rate
        if i % decay_time == 0:
            learning_rate *= decay_rate
            optimizer.lr = learning_rate

        save_model(model, f"neural_models/network_v2_epoch_{i}.pt")

    # write losses to file
    with open('losses.txt', 'w') as f:
        f.write(" ".join(losses))

def save_model(model, filename):
    """ Save the model's state dict to file """
    torch.save(model.state_dict(), filename)


def load_model(filename, training=False):
    """ Load the model's state dict from file. Must init the base model first. """
    model = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)
    model.load_state_dict(torch.load(filename))
    # only call eval() if NOT training
    # otherwise if using the model for evaluation (testing - no more training) use eval()
    if training:
        model.train()
    else:
        model.eval()
    return model


def create_self_hand_tensor(our_hand: List) -> torch.Tensor:
    """ Create tensor of the current hand and normalize it (1x13) """
    cur_hand = [val / DECK_SIZE for val in our_hand]
    return torch.FloatTensor(cur_hand, device=device)


def create_opp_hand_tensor(opponent_hand: List) -> torch.Tensor:
    """ Create tensor of an opponent's hand and normalize it (1x13) """
    opp_hand = [val / DECK_SIZE for val in opponent_hand]
    return torch.FloatTensor(opp_hand, device=device)


def create_opp_size_tensor(hand_size: int) -> torch.Tensor:
    """ Create a 1x1 tensor of an opponent's hand size """
    return torch.FloatTensor([hand_size / DECK_SIZE], device=device)


def create_other_opp_hand_tensor(other_opponents: List) -> torch.Tensor:
    """ Create a 1x13 combined tensor of the other opponents hands """
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES)
    for opp in other_opponents:
        tensor.add_(create_opp_hand_tensor(opp))
    return tensor


def create_other_opp_size_tensor(other_opponents_sizes: List) -> torch.Tensor:
    """ Create a 1x1 combined tensor of the other opponents hand size """
    tensor = torch.zeros(1)
    for opp_size in other_opponents_sizes:
        tensor.add_(create_opp_size_tensor(opp_size))
    return tensor


def create_a_four_tensor(fours: Iterable[str]) -> torch.Tensor:
    """ Create a 1x13 tensor given a player's fours"""
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES, device=device)
    for card in fours:
        i = CARD_VALUE_TENSOR_INDEX_DICT[card]
        tensor[i] = SUITS / DECK_SIZE
    return tensor


def create_fours_tensor(current_fours: List, opponents_fours: List) -> torch.Tensor:
    """ Create a 1x13 fours tensor given the current bot player and other opponents """
    tensor = torch.FloatTensor(create_a_four_tensor(current_fours))
    for opp_fours in opponents_fours:
        tensor.add_(create_a_four_tensor(opp_fours))
    return tensor


def create_deck_size(deck_size: int) -> torch.Tensor:
    """ Create the deck size tensor as a 1x1 tensor"""
    return torch.FloatTensor([deck_size / DECK_SIZE], device=device)


def create_asked_card_tensor(asked_card: str) -> torch.Tensor:
    """ Create the asked card tensor as a 1x13 tensor"""
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES, device=device)
    index = CARD_VALUE_TENSOR_INDEX_DICT[asked_card]
    tensor[index] = 1.0
    return tensor


if __name__ == "__main__":
    # load from the pickle file
    # this is the cleaned data with the converted lists
    df = pd.read_pickle("cleaned_rounds_data.pkl")

    # NOTES:
    # learning rate may be need to be lowered
    # total epochs taken might be 10 or a little over that
    # decay_rate of 0.25 next
    # losses file: 12 sets of loss per epoch

    # set up params for network model
    model = load_model("neural_models/network_v1.pt", training=True)
    # load model state dict HERE if need to train more
    loss_fn = torch.nn.MSELoss(reduction='sum')
    

    learning_rate = 0.05
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    start_train_session(df, model, loss_fn, optimizer=optimizer, epoch=5, decay_rate=0.25, decay_time=1, learning_rate=learning_rate)
