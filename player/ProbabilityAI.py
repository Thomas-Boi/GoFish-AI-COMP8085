from player.OppAwareAI import *
from player.Opponent import *
from Deck import SUITS, DECK_SIZE
import math
import pandas as pd
import random


"""
The turn when we start calculating the probability of
the card we are going to ask.
"""
TURN_TO_START_PROB_AI = 5

"""
Used to separate a card value and a name.
"""
CARD_NAME_SEPERATOR = "_"

class ProbabilityAI(OppAwareAI):

    def __init__(self, name: str) -> None:
        """
        Represents an AI that is aware of its opponents.
        This tracks the amount of cards that a player has in their hand.
        This serves as the base class for more complex AI.

        This only tracks the minimum amount of cards that the opponent has.
        This is due to the unknown nature of asking. A player asking for a card
        might have 1-3 cards of those values. However, we don't know the exact number.
        The only time we know the exact number is when they successfully ask for a card
        and the other player gave them those cards. We do not know when a card is gained
        through fishing.
        """
        super().__init__(name)

        """
        Track how many turns have passed.
        """
        self.turn_counter = 0

    def update_player_state(self, move: Move):
        """
        Update the state of the player based on a move.
        """
        # check whether the player found a four => if they did, remove all
        # cards from the game with that value.
        if move.found_fours is not None:
            for opp in self.opponents.values():
                opp.remove_card(move.found_fours)
            # don't do anything else afterwards cause there's no need
            # a four of a kind removes all values like that from the game
            return

        # regardless whether the ask was successful, we know that player has at least
        # 1 card of that value. 
        if move.asker != self.name:
            # if the card is not 0 (already counted), do nothing
            # since we can't tell exactly how many cards are in that player's hand
            # and can only track the minimum aka "at least" amount of that value
            # in hand. Thus, if not tracked yet, add 1 to the card counter.
            # Else, we aren't sure.
            if not self.opponents[move.asker].has_card(move.card): 
                self.opponents[move.asker].give_cards(move.card)

        # only updates if ask was successful, else nothing happens
        if move.ask_succeed:
            # check who ask for what => if it's us, don't need to update
            # since the Game updates us already and we know our own stats
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card, move.amount)
                
            if move.target != self.name:
                self.opponents[move.target].remove_card(move.card)  
            return

        # here, we know that the ask didn't succeed

        if move.fish_succeed:
            if move.asker != self.name:
                self.opponents[move.asker].give_cards(move.card)


    def make_move(self, other_players: Tuple[OppStat], deck_count: int) -> Move:
        """
        Make a move and ask a player for a card.
        :return a tuple of target player, which is a number, and a card
        to ask that player.
        """
        self.turn_counter += 1
        if self.turn_counter > TURN_TO_START_PROB_AI:
            return self.make_random_move(other_players)


        # contains the most probable card of each player
        best_prob_table = pd.DataFrame()
        for opp in self.opponents.values():
            prob_table = self.generate_prob_table(opp, other_players, deck_count)
            best_card_for_opp = self.find_best_card(prob_table)
            # add this as a column
            # to address same value from different players, append them
            best_prob_table.loc[:, f"{best_card_for_opp.name}{CARD_NAME_SEPERATOR}{opp.name}"] = best_card_for_opp
        
        # find best column with the best card
        best_card = self.find_best_card(best_prob_table)
        # retrieve the card name and opp name
        card, opp_name = str(best_card.name).split(CARD_NAME_SEPERATOR)

        # fill out opp_name properly later
        return Move(self.name, opp_name, card) 

    def generate_prob_table(self, opp: Opponent, opponents: Tuple[OppStat], deck_count: int) -> pd.DataFrame:
        """
        Create the probability table for the opponent for only the cards
        that we currently possessed.
        :param opp: the opponent we are checking.
        :param opponents: stats that know about from other opponents (hand_size and fours).
        :param deck_count: the number of cards remaining in the deck.
        """
        # we are checking probability of having 1 of, 2 of, and 3 of a certain card value
        target_amounts = list(range(1, 4))

        # default table
        table = pd.DataFrame(index=target_amounts)

        # this specific opponent's opp stat
        opp_stat = [opp_stat for opp_stat in opponents if opp_stat.name == opp.name][0]

        # fill out the table
        for card, card_amount in self.hand.items():
            # don't have any card => can't ask this
            if card_amount == 0:
                continue

            for target_amount in target_amounts:
                # fill out anything we know for sure first (cards they have asked)
                # recall opp only tracks at least => we will treat it as exact cause there's no
                # other info.
                
                # if we know opp has asked for this card and know that they have at least
                # this amount or more. E.g we know they have at least two of 5s (asked for 5, got a 5)
                # => [1, 5] and [2, 5] should have prob of 1
                if opp.hand[card] >= target_amount:
                    table.loc[target_amount, card] = 1 # for sure they have that card
                    continue

                remaining_amount = self.find_remaining_amount(card, opponents)

                # get the hand size needed
                hand_size = opp_stat.hand_size
                for count in opp.hand.values():
                    # decrease hand size if it contains card we know about
                    hand_size -= count

                # get the pool we are selecting from
                pool = self.find_pool_size(opponents)
                table.loc[target_amount, card] = self.find_prob_of_card(target_amount, remaining_amount, hand_size, pool)

        return table

    def find_remaining_amount(self, target: str, opps: Tuple[OppStat]):
        """
        Find all the amount of card left that's not accounted for (aka not in anyone's hand).
        :param target, the card we are looking for.
        :param opps, the opponents.
        """
        # get the amount of the card we're searching for that's left
        remaining_amount = SUITS

        # see if the bot is holding any
        remaining_amount -= self.hand[target] # remove anything that we hold

        # remove any amount that the opponents holds
        for opp in self.opponents.values():
            remaining_amount -= opp.hand[target] # remove anything that the opp holds

        return remaining_amount

    def find_pool_size(self, opps: Tuple[OppStat]):
        """
        Find the size of the pool of cards we are selecting from.
        This means all the cards that are unknown.
        :param opps: all the other opponents.
        """
        pool_size = DECK_SIZE

        # our cards and fours
        pool_size -= self.get_hand_size()
        for card in self.fours:
            pool_size -= 4 # four of a kind == 4 cards each value

        # do the same for opponents
        for opp in opps:
            pool_size -= opp.hand_size
            for card in opp.fours:
                pool_size -= 4

        return pool_size

    def find_prob_of_card(self, match_amount: int, 
                          match_remaining_amount: int,
                          hand_size: int, pool_size: int) -> float:
        """
        Find the probability of a certain amount_of_cards existing in 
        a given hand size knowing all the pertinent information. This assumes
        that the order of checking the opponents does not matter.
        :param match_amount, the amount of the card value we are checking for.
        :param match_remaining_amount, the remaining amount of cards left for the card we're looking for.
        :param hand_size, the hand size.
        :param pool_size, the total amount of cards we are picking from. This includes the hand_size
        as well.
        """
        matching_value = math.comb(match_remaining_amount, match_amount)
        # short circuit to save time
        if matching_value == 0:
            return 0 

        non_matching_value = math.comb(pool_size - match_remaining_amount, hand_size - match_amount)
        total = math.comb(pool_size, hand_size)
        return matching_value * non_matching_value / total

    def find_best_card(self, prob_table: pd.DataFrame) -> pd.Series:
        """
        Find the best possible card to ask for based on the prob table
        passed in. 
        :param prob_table, a probability table with 3 rows (index=[1,2,3])
        and the columns are the card values (2, 3, J, Q, K, etc.). The values
        are the probability of certain amount of card being present.
        :return: this returns a series with all the probability (1 of, 2 of, 3 of)
        of the best card. The series's name is the card's value.
        """
        # method: 
        # - start with the most likely cases: row 1 aka having 1 of value in hand.
        # - If one is the best => return that 
        # - If more than one is equal => move on to the next case
        # e.g if one of 2 and one of J has the same odds, evaluate two of 2s and two of Js.

        if prob_table.empty:
            raise ValueError("Empty probability table. This should not happen.")

        candidates = []
        highest_prob = 0

        for row in prob_table.iterrows():
            index, data = row

            # if first row => find the best one with no filter
            if index == 1:
                for card, prob in data.iteritems():
                    if prob > highest_prob:
                        highest_prob = prob
                        candidates = [card]
                    elif prob == highest_prob:
                        candidates.append(card) # multiple card shares the same prob

            # else, only search the columns that are in the candidates
            else:
                for card in candidates:
                    prob = data[str(card)]
                    if prob > highest_prob:
                        highest_prob = prob
                        candidates = [card]
                    elif prob == highest_prob:
                        candidates.append(card) # multiple card shares the same prob

            # 1 best solution => we will go for it
            # should never have 0 candidates
            if len(candidates) == 1:
                return prob_table.loc[:, str(candidates[0])]

        # if we are here, there are still two or more equal choices => pick a random one
        return prob_table.loc[:, str(random.choice(candidates))]
