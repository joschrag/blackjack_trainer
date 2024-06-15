import datetime
import random

import numpy as np
import pandas as pd

from basic_strategy import engine
from basic_strategy.card_eval import card_eval
from basic_strategy.hand import Card, Hand, deck

CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
ENDC = "\033[0m"
OKGREEN = "\033[92m"
FAIL = "\033[91m"
if __name__ == "__main__":
    user = input("Input your username:")
    while True:
        dealt_cards = random.sample(deck, k=3)
        hand, dealer = Hand(dealt_cards[0:2]), dealt_cards[2]
        print(
            f"Your hand: '{",".join([str(c) for c in hand.cards])}' | Dealer upcard: {dealer}"
        )
        choice = input("Your choice: ")
        correct = card_eval(hand, dealer)
        if choice == correct:
            print(f"{OKGREEN}success{ENDC}")
        else:
            print(f"{FAIL}{correct}{ENDC}")
        # TODO Add involved cards
        df = pd.DataFrame(
            {
                "user": pd.Series([user], dtype=pd.StringDtype()),
                "training_type": pd.Series(["card_eval"], dtype=pd.StringDtype()),
                "was_correct": pd.Series([choice == correct], dtype=pd.BooleanDtype()),
                "correct_move": pd.Series([correct], dtype=pd.StringDtype()),
                "guessed_move": pd.Series([choice], dtype=pd.StringDtype()),
                "card1": pd.Series([hand.cards[0].rank], dtype=pd.StringDtype()),
                "card2": pd.Series([hand.cards[1].rank], dtype=pd.StringDtype()),
                "hand_value": pd.Series([hand.value], dtype=pd.Int32Dtype()),
                "dealer_card": pd.Series([dealer.value], dtype=pd.Int32Dtype()),
                "upload_time": pd.Series(
                    [datetime.datetime.now()], dtype="datetime64[ns]"
                ),
            }
        )
        with engine.begin() as conn:
            df.to_sql("training_data", conn, if_exists="append")
