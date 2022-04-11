import ast
import math
import pickle
import pandas as pd
import torch.nn as nn
import torch

from typing import List, Iterable

from Deck import SUITS
from util import device
from player.NeuralNetworkAI import NeuralNetworkAI
from player.NeuralNetPlayer import DECK_SIZE, AMOUNT_OF_CARD_VALUES, CARD_VALUE_TENSOR_INDEX_DICT

MODEL_FILE_V1 = "network_v1"
LOSS_FILE = "losses.txt"
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


def start_train_session(dataframe, model, loss_fn, optimizer=None, learning_rate=0.05,
                        epoch=500, decay_rate=0.5, decay_time=50):
    last_loss = 0
    updated_model = model
    losses = []

    for i in range(1, epoch + 1):
        print(f"Epoch {i}")
        print("Saving and reloading saved model...")

        new_model_str = f"{MODEL_FILE_V1}_{i}.pt"
        save_model(updated_model, new_model_str)
        updated_model = load_model(new_model_str)

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
                              updated_model, learning_rate, loss_fn,
                              optimizer=optimizer)

            if index % 100000 == 0:
                losses.append(last_loss.item())
                print(f"{index}: {last_loss.item()}")


        # stop early if we have low loss or if the loss exploded
        if last_loss <= 0.01:
            break
        elif last_loss == math.inf or last_loss == -math.inf:
            break

        # decay the learning rate
        if i % decay_time == 0:
            learning_rate *= decay_rate

            if optimizer:
                optimizer.lr = learning_rate

    print(losses)
    with open('losses.txt', 'w') as f:
        for item in losses:
            f.write(f"{item} ")

def save_model(model, filename):
    torch.save(model.state_dict(), filename)


def load_model(filename):
    model = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)
    model.load_state_dict(torch.load(filename))
    model.eval()
    return model


def create_self_hand_tensor(our_hand: List) -> torch.Tensor:
    cur_hand = [val / DECK_SIZE for val in our_hand]
    return torch.FloatTensor(cur_hand, device=device)


def create_opp_hand_tensor(opponent_hand: List) -> List[torch.Tensor]:
    opp_hand = [val / DECK_SIZE for val in opponent_hand]
    return torch.FloatTensor(opp_hand, device=device)


def create_opp_size_tensor(hand_size: int) -> List[torch.Tensor]:
    return torch.FloatTensor([hand_size / DECK_SIZE], device=device)


def create_other_opp_hand_tensor(other_opponents: List) -> List[torch.Tensor]:
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES)
    for opp in other_opponents:
        tensor.add_(create_opp_hand_tensor(opp))
    return tensor


def create_other_opp_size_tensor(other_opponents_sizes: List) -> List[torch.Tensor]:
    tensor = torch.zeros(1)
    for opp_size in other_opponents_sizes:
        tensor.add_(create_opp_size_tensor(opp_size))
    return tensor


def create_a_four_tensor(fours: Iterable[str]) -> torch.Tensor:
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES, device=device)
    for card in fours:
        i = CARD_VALUE_TENSOR_INDEX_DICT[card]
        tensor[i] = SUITS / DECK_SIZE
    return tensor


def create_fours_tensor(current_fours: List, opponents_fours: List) -> List[torch.Tensor]:
    tensor = torch.FloatTensor(create_a_four_tensor(current_fours))
    for opp_fours in opponents_fours:
        tensor.add_(create_a_four_tensor(opp_fours))
    return tensor


def create_deck_size(deck_size: int) -> torch.Tensor:
    return torch.FloatTensor([deck_size / DECK_SIZE], device=device)


def create_asked_card_tensor(asked_card: str) -> List[torch.Tensor]:
    tensor = torch.zeros(AMOUNT_OF_CARD_VALUES, device=device)
    index = CARD_VALUE_TENSOR_INDEX_DICT[asked_card]
    tensor[index] = 1.0
    return tensor


if __name__ == "__main__":
    # load from the pickle file
    # this is the cleaned data with the converted lists
    df = pd.read_pickle("cleaned_rounds_data.pkl")

    # set up params for network model
    model = NeuralNetworkAI(INPUT_SIZE, OUTPUT_SIZE)
    loss_fn = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

    # NOTES:
    # learning rate may be need to be lowered
    # total epochs taken might be 10 or a little over that
    # decay_rate of 0.25 next

    start_train_session(df, model, loss_fn, optimizer=optimizer, epoch=5, decay_rate=0.25, decay_time=1)
