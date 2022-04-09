from typing import Dict

import pandas as pd

COLUMN_NAMES = ["our_hand", "our_fours", "opp_0_cards", "opp_0_hand_size", "opp_0_fours",
                "opp_1_cards", "opp_1_hand_size", "opp_1_fours",
                "opp_2_cards", "opp_2_hand_size", "opp_2_fours",
                "deck_size", "successful_ask", "card_ask"]

class Database():
    def __init__(self):
        self.data_list = []
        self.main_df = pd.DataFrame
        self.temp_df = pd.DataFrame(columns=COLUMN_NAMES)

    def write_csv(self):
        self.temp_df = pd.json_normalize(self.data_list)

        result = pd.concat([self.main_df, self.temp_df], ignore_index=True)
        result.to_csv('rounds_data.csv', index=False)

    def read_csv(self):
        try:
            self.main_df = pd.read_csv("rounds_data.csv")
            #self.data_list = self.main_df.to_dict('records')
        except (OSError, IOError) as e:
            self.main_df = pd.DataFrame(columns=COLUMN_NAMES)

    def append_row(self, input_output_dict: Dict):
        # opponents starting from index 0 since its simpler

        # A row structure is the following:
        # our_hand | our_fours | opp_0_cards | opp_0_hand_size | opp_0_fours
        # | opp_1_cards | opp_1_hand_size | opp_1_fours
        # | opp_2_cards | opp_2_hand_size | opp_2_fours
        # | deck_size | successful_ask | card_ask

        self.data_list.append(input_output_dict)
