"""This module initializes the database and contains the other submodules."""

import pathlib
import sys

import pandas as pd
import sqlalchemy as sa

from .setup_logging import (  # noqa: F401
    NonErrorFilter,
    setup_logging,
    setup_logging_3_11,
)

db_file = pathlib.Path.cwd() / "db" / "db.sqlite"
if not db_file.exists():
    db_file.touch()
engine = sa.create_engine("sqlite:///db/db.sqlite")

# Check if the Python version is 3.9
if sys.version_info.major == 3 and sys.version_info.minor == 9:
    setup_logging_3_11()
else:
    setup_logging()

STANDARD_SETTINGS = pd.DataFrame(
    {
        "setting": pd.Series(
            [
                "auto_deal",
                "shoe_game",
                "das_game",
                "split_aces",
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

if not sa.inspect(engine).has_table("settings"):
    with engine.begin() as conn:
        STANDARD_SETTINGS.to_sql("settings", conn, index=False)

TABLE_DTYPES = {
    "user": pd.StringDtype(),
    "training_type": pd.StringDtype(),
    "was_correct": pd.BooleanDtype(),
    "correct_move": pd.StringDtype(),
    "guessed_move": pd.StringDtype(),
    "card1": pd.StringDtype(),
    "card2": pd.StringDtype(),
    "hand_value": pd.Int16Dtype(),
    "dealer_card": pd.Int16Dtype(),
    "upload_time": "datetime64[ns]",
}

EXT_TABLE_DTYPES = {**TABLE_DTYPES, "date": "datetime64[ns]", "count": pd.Int32Dtype(), "total": pd.Int32Dtype()}

SETTING_DTYPES = [bool, int, bool, bool, bool, int, int, int, int]
