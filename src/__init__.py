"""This module initializes the database and contains the other submodules."""

import pathlib

import pandas as pd
import sqlalchemy as sa

db_file = pathlib.Path.cwd() / "db" / "db.sqlite"
if not db_file.exists():
    db_file.touch()
engine = sa.create_engine("sqlite:///db/db.sqlite")

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
