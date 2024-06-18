"""This script contains the callbacks used in the app ui generation."""

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from src import engine
from src.stats.create_plots import main_plot


@callback(Output("data_store", "data"), Input("1_min", "n_intervals"))
def load_data(_: int) -> list:
    """Load data from the database every 1 minute.

    Args:
        _ (int): trigger to execute function

    Returns:
        list: data read from database
    """
    with engine.begin() as conn:
        dataframe = pd.read_sql_table("training_data", conn).drop(columns=["index"])
    dataframe["date"] = dataframe["upload_time"].dt.date
    dataframe["count"] = 1
    dataframe["total"] = 1
    return dataframe.to_dict("records")


@callback(Output("user_dd", "disabled"), Input("user_switch", "checked"))
def activate_user_dropdown(switch: bool) -> bool:
    """Switch the user dropdown on and off.

    Args:
        switch (bool): switch input on?

    Returns:
        bool: disable user dropdown?
    """
    return not switch


@callback(Output("mode_dd", "disabled"), Input("mode_switch", "checked"))
def activate_mode_dropdown(switch: bool) -> bool:
    """Switch the mode dropdown on and off.

    Args:
        switch (bool): switch input on?

    Returns:
        bool: disable mode dropdown?
    """
    return not switch


@callback(Output("move_dd", "disabled"), Input("move_switch", "checked"))
def activate_move_dropdown(switch: bool) -> bool:
    """Switch the move dropdown on and off.

    Args:
        switch (bool): switch input on?

    Returns:
        bool: disable move dropdown?
    """
    return not switch


@callback(
    Output("stat_graphs", "children"),
    Input("data_store", "data"),
    Input("user_switch", "checked"),
    Input("mode_switch", "checked"),
    Input("move_switch", "checked"),
    Input("user_dd", "value"),
    Input("mode_dd", "value"),
    Input("move_dd", "value"),
    Input("abs_val_dd", "value"),
)
def plot_data_callback(
    data: list,
    split_user: bool,
    split_mode: bool,
    split_move: bool,
    user_dd: list,
    mode_dd: list,
    move_dd: list,
    abs_val: str,
) -> list:
    """Plot the aggregated move data over different days.

    Args:
        data (list): blackjack move data
        split_user (bool): split into different graphs per user?
        split_mode (bool): split into different graphs per mode?
        split_move (bool): split into different bars per move?
        user_dd (list): selected users
        mode_dd (list): selected modes
        move_dd (list): selected moves
        abs_val (str): show absolute values or percentages

    Returns:
        list: list of all graphs
    """
    if data:
        if not split_user:
            user_dd = []
        if not split_mode:
            mode_dd = []
        if not split_move:
            move_dd = []
        fig_dict = main_plot(data, user_dd, mode_dd, move_dd, abs_val == "absolute values")
        graphs = [
            [dbc.Row(html.H1(f"{user} {mode}")), dbc.Row([dbc.Col(dcc.Graph(figure=graph))])]
            for user, d in fig_dict.items()
            for mode, graph in d.items()
        ]
        return [item for sublist in graphs for item in sublist]
    return []


@callback(Output("user_dd", "options"), Input("data_store", "data"), prevent_initial_callback=True)
def populate_user_dropdown(data: list) -> list:
    """Set available options for user dropdown.

    Args:
        data (list): blackjack move data

    Returns:
        list: available user
    """
    if data:
        dataframe = pd.DataFrame(data)
        return dataframe.user.unique().tolist()
    return []


@callback(
    Output("mode_dd", "options"),
    Input("data_store", "data"),
    prevent_initial_callback=True,
)
def populate_mode_dropdown(data: list):
    """Set available options for mode dropdown.

    Args:
        data (list): blackjack move data

    Returns:
        list: available modes
    """
    if data:
        dataframe = pd.DataFrame(data)
        return dataframe.training_type.unique().tolist()
    return []
