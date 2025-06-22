"""Test settings callback funtionality."""

from collections import Counter
from contextvars import copy_context

import pandas as pd
import pytest
import sqlalchemy as sa
from dash._callback_context import context_value
from dash._utils import AttributeDict

from blackjack_trainer import SETTING_DTYPES
from blackjack_trainer.app import settings_callbacks as sc
from tests.fixtures import setup_db  # noqa: F401


@pytest.mark.parametrize(
    "input_data",
    [
        {"settings": {}},
        {"settings": {"auto_deal": False}, "trigger": [("auto_deal", "checked")]},
        {"settings": {"shoe_game": 2}, "trigger": [("shoe_size_game", "value")]},
        {"settings": {"shoe_game": 3}, "trigger": [("shoe_size_game", "value")]},
        {"settings": {"das_game": False}, "trigger": [("das_game", "value")]},
        {"settings": {"split_aces_game": False}, "trigger": [("split_aces_game", "checked")]},
        {"settings": {"dealer_soft": True}, "trigger": [("dealer_soft", "checked")]},
        {"settings": {"split_game": 1}, "trigger": [("split_num_game", "value")]},
        {"settings": {"split_game": 2}, "trigger": [("split_num_game", "value")]},
        {"settings": {"split_game": 3}, "trigger": [("split_num_game", "value")]},
        {"settings": {"double_game": 2}, "trigger": [("double_game", "value")]},
        {"settings": {"double_game": 3}, "trigger": [("double_game", "value")]},
        {"settings": {"shoe_train": 2}, "trigger": [("shoe_size_train", "value")]},
        {"settings": {"shoe_train": 3}, "trigger": [("shoe_size_train", "value")]},
        {"settings": {"das_train": 2}, "trigger": [("das_train", "value")]},
        {"settings": {"das_train": 3}, "trigger": [("das_train", "value")]},
    ],
)
def test_cb_eval_action(setup_db, mocker, input_data: dict) -> None:  # noqa: F811  # noqa:F811
    engine, _ = setup_db
    mocker.patch("blackjack_trainer.app.game_callbacks.engine", engine)
    table = sa.Table("settings", sa.MetaData(), autoload_with=engine)
    stmt = sa.select(table)
    with engine.begin() as conn:
        base_df = pd.read_sql(
            stmt,
            conn,
        )
    base_dict = {row["setting"]: dtype(row["value"]) for (_, row), dtype in zip(base_df.iterrows(), SETTING_DTYPES)}
    test_dict = base_dict | input_data["settings"]

    def run_callback() -> tuple[list, list, list]:
        context_value.set(
            AttributeDict(
                **{
                    "triggered_inputs": [
                        {"prop_id": f"{trigger}.{attr}"} for trigger, attr in input_data.get("trigger", [])
                    ]
                }
            )
        )
        return sc.update_settings(**test_dict, settings=[base_dict])

    ctx = copy_context()
    output, *_ = ctx.run(run_callback)
    assert Counter(output[0]) == Counter(test_dict)
