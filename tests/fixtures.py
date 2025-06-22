"""This script contains pytest test fixtures."""

import datetime
from typing import Generator

import pandas as pd
import pytest
import sqlalchemy as sa


@pytest.fixture(scope="session")
def setup_db() -> Generator[tuple[sa.engine.Engine, pd.DataFrame], None, None]:
    df = pd.DataFrame(
        {
            "user": pd.Series(["user1", "user2", "user1", "user2", "user1"], dtype=pd.StringDtype()),
            "training_type": pd.Series(["basic", "basic", "soft", "hard", "split"], dtype=pd.StringDtype()),
            "was_correct": pd.Series([True, True, False, False, True], dtype=pd.BooleanDtype()),
            "correct_move": pd.Series(["d", "sur", "ds", "d", "spl"], dtype=pd.StringDtype()),
            "guessed_move": pd.Series(["d", "sur", "d", "h", "spl"], dtype=pd.StringDtype()),
            "card1": pd.Series(["3", "A", "A", "5", "2"], dtype=pd.StringDtype()),
            "card2": pd.Series(["5", "5", "8", "6", "2"], dtype=pd.StringDtype()),
            "hand_value": pd.Series([8, 16, 19, 11, 4], dtype=pd.Int16Dtype()),
            "dealer_card": pd.Series([4, 9, 6, 11, 4], dtype=pd.Int16Dtype()),
            "upload_time": pd.Series([datetime.datetime.now()] * 5, dtype="datetime64[ns]"),
        }
    )
    STANDARD_SETTINGS = pd.DataFrame(
        {
            "setting": pd.Series(
                [
                    "auto_deal",
                    "shoe_game",
                    "das_game",
                    "split_aces_game",
                    "dealer_soft",
                    "split_game",
                    "double_game",
                    "shoe_train",
                    "das_train",
                ],
                dtype=pd.StringDtype(),
            ),
            "value": pd.Series(
                [
                    False,
                    1,
                    True,
                    True,
                    False,
                    4,
                    1,
                    1,
                    0,
                ]
            ),
        }
    )

    engine = sa.create_engine("sqlite://")
    with engine.begin() as conn:
        df.to_sql("training_data", conn, if_exists="append")
        STANDARD_SETTINGS.to_sql("settings", conn, index=False)
    yield engine, df
