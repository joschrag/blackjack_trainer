import datetime
from collections import Counter
from typing import Generator

import pandas as pd
import pytest
import sqlalchemy as sa

from src import EXT_TABLE_DTYPES
from src.app import ui_callbacks as ui


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
    engine = sa.create_engine("sqlite://")
    with engine.begin() as conn:
        df.to_sql("training_data", conn, if_exists="append")
    yield engine, df


def test_cb_load_data(setup_db: tuple[sa.engine.Engine, pd.DataFrame]) -> None:
    engine, df = setup_db
    data = ui.load_data(1, engine)
    df["date"] = df["upload_time"].dt.date
    df["count"] = 1
    df["total"] = 1
    data_df = pd.DataFrame(data).astype(EXT_TABLE_DTYPES)
    pd.testing.assert_frame_equal(data_df, df.astype(EXT_TABLE_DTYPES))


@pytest.mark.parametrize("status", [True, False])
def test_cb_activate_user_dropdown(status: bool) -> None:
    res = ui.activate_user_dropdown(status)
    assert res is not status


@pytest.mark.parametrize("status", [True, False])
def test_cb_activate_mode_dropdown(status: bool) -> None:
    res = ui.activate_mode_dropdown(status)
    assert res is not status


@pytest.mark.parametrize("status", [True, False])
def test_cb_activate_move_dropdown(status: bool) -> None:
    res = ui.activate_move_dropdown(status)
    assert res is not status


@pytest.mark.parametrize("user_switch,user_list", zip([True, False], [["user1", "user2"], []]))
@pytest.mark.parametrize("mode_switch,mode_list", zip([True, False], [["hard", "basic"], []]))
@pytest.mark.parametrize("move_switch,move_list", zip([True, False], [["h", "sur"], []]))
@pytest.mark.parametrize("do_abs_vals", ["absolute values", "percent"])
def test_cb_plot_data_callback(
    setup_db: tuple[sa.engine.Engine, pd.DataFrame],
    user_switch: bool,
    mode_switch: bool,
    move_switch: bool,
    user_list: list,
    mode_list: list,
    move_list: list,
    do_abs_vals: str,
) -> None:
    _, df = setup_db
    df["date"] = df["upload_time"].dt.date
    df["count"] = 1
    df["total"] = 1
    df = df.astype(EXT_TABLE_DTYPES)
    graphs = ui.plot_data_callback(
        df.to_dict("records"), user_switch, mode_switch, move_switch, user_list, mode_list, move_list, do_abs_vals
    )
    assert len(graphs) == 2 * max(1, len(user_list)) * max(1, len(mode_list))


def test_cb_populate_user_dropdown(setup_db: tuple[sa.engine.Engine, pd.DataFrame]) -> None:
    _, df = setup_db
    df["date"] = df["upload_time"].dt.date
    df["count"] = 1
    df["total"] = 1
    df = df.astype(EXT_TABLE_DTYPES)
    users = ui.populate_user_dropdown(df.to_dict("records"))
    assert Counter(users) == Counter(["user1", "user2"])


def test_cb_populate_mode_dropdown(setup_db: tuple[sa.engine.Engine, pd.DataFrame]) -> None:
    _, df = setup_db
    df["date"] = df["upload_time"].dt.date
    df["count"] = 1
    df["total"] = 1
    df = df.astype(EXT_TABLE_DTYPES)
    mode = ui.populate_mode_dropdown(df.to_dict("records"))
    assert Counter(mode) == Counter(["basic", "soft", "hard", "split"])
