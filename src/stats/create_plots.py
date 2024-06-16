from typing import Optional

import pandas as pd
from plotly import graph_objects as go

from src import engine

COLOR_DICT = {
    "d": "#00ff00",
    "ds": "#00ccff",
    "s": "#3333ff",
    "h": "#ff0000",
    "spl": "#ff6600",
    "sur": "#cc00cc",
    "das": "#5d2703",
    "False": "#ff0000",
    "True": "#00ff00",
}


def get_data() -> pd.DataFrame:
    with engine.begin() as conn:
        dataframe = pd.read_sql_table("training_data", conn).drop(columns=["index"])
    dataframe["date"] = dataframe["upload_time"].dt.date
    dataframe["count"] = 1
    dataframe["total"] = 1
    return dataframe


def filter_data(
    dataframe: pd.DataFrame,
    user_list: Optional[list] = None,
    mode_list: Optional[list] = None,
    move_list: Optional[list] = None,
) -> pd.DataFrame:
    if user_list:
        dataframe = dataframe.loc[dataframe.user.isin(user_list)]
    if mode_list:
        dataframe = dataframe.loc[dataframe.training_type.isin(mode_list)]
    if move_list:
        dataframe = dataframe.loc[dataframe.correct_move.isin(move_list) | dataframe.guessed_move.isin(move_list)]
    return dataframe


def set_optional_lists(user_switch, mode_switch, move_switch, absolute_value) -> tuple[list, str]:
    group_list = ["date"]
    if user_switch:
        group_list += ["user"]
    if move_switch:
        group_list += ["correct_move"]
    if mode_switch:
        group_list += ["training_type"]
    if absolute_value:
        y_column = "count"
    else:
        y_column = "percent"
    return group_list, y_column


def transform_data(dataframe: pd.DataFrame, group_list: list) -> pd.DataFrame:
    df_g1 = dataframe.groupby(group_list + ["was_correct"], as_index=False)["count"].count()
    df_g2 = dataframe.groupby(group_list, as_index=False)["total"].count()
    df_g = df_g1.merge(df_g2, on=group_list, how="inner").reset_index(drop=True)
    return df_g


def plot_figure(
    dataframe: pd.DataFrame,
    data_col: str,
    user_list: Optional[list] = None,
    mode_list: Optional[list] = None,
    move_list: Optional[list] = None,
) -> dict[str, dict[str, go.Figure]]:
    fig_dict: dict = {}
    if user_list:
        user_df_dict = {user: dataframe.loc[dataframe.user == user, :].copy() for user in user_list}
    else:
        user_df_dict = {"all user": dataframe}
    for user, dataframe in user_df_dict.items():
        fig_dict[user] = {}
        if mode_list:
            mode_df_dict = {mode: dataframe.loc[dataframe.training_type == mode, :].copy() for mode in mode_list}
        else:
            mode_df_dict = {"all_modes": dataframe}
        for mode, dataframe in mode_df_dict.items():
            fig = go.Figure()
            legend_dict = dict.fromkeys(dataframe.was_correct.unique(), True)
            if move_list:
                legend_dict_move = dict.fromkeys(dataframe.correct_move.unique(), True)
            for val in dataframe.was_correct.unique():
                df_f = dataframe.loc[dataframe.was_correct == val, :].copy()
                if move_list:
                    for typ in df_f.correct_move.unique():
                        df_p = df_f.loc[df_f.correct_move == typ].copy()
                        df_p.loc[:, "percent"] = df_f.loc[:, "count"] / df_f.loc[:, "total"]
                        fig.add_trace(
                            go.Bar(
                                x=df_p["date"],
                                y=df_p[data_col],
                                marker={"color": COLOR_DICT[typ]},
                                name=f"{typ}",
                                legendgroup=f"{typ}",
                                showlegend=legend_dict_move[typ],
                            )
                        )
                        legend_dict_move[typ] = False
                else:
                    df_f.loc[:, "percent"] = df_f.loc[:, "count"] / df_f.loc[:, "total"]
                    fig.add_trace(
                        go.Bar(
                            x=df_f["date"],
                            y=df_f[data_col],
                            name=f"{val}",
                            marker={"color": COLOR_DICT[f"{val}"]},
                            legendgroup=f"{val}",
                            showlegend=legend_dict[val],
                        )
                    )
                    legend_dict[val] = False
            fig_dict[user][mode] = fig
    return fig_dict


def main_plot(
    data: Optional[list] = None,
    user_dd: Optional[list] = None,
    mode_dd: Optional[list] = None,
    move_dd: Optional[list] = None,
    absolute_val_check: bool = True,
) -> dict[str, dict[str, go.Figure]]:
    if data:
        dataframe = pd.DataFrame(data)
    else:
        dataframe = get_data()
    dataframe = filter_data(dataframe, user_dd, mode_dd, move_dd)
    group_list, data_column = set_optional_lists(bool(user_dd), bool(mode_dd), bool(move_dd), absolute_val_check)
    dataframe = transform_data(dataframe, group_list)
    fig_dict = plot_figure(dataframe, data_column, user_dd, mode_dd, move_dd)
    return fig_dict
