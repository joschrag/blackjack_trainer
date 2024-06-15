import pandas as pd
import plotly
from plotly import graph_objects as go

from src import engine

COLOR_DICT = {
    "d": "#00ff00",
    "ds": "#00ccff",
    "s": "#3333ff",
    "h": "#ff0000",
    "spl": "#ff6600",
    "sur": "#cc00cc",
    "False":"#ff0000",
    "True":"#00ff00"
}

view_move_types = False
view_training_types = False
view_absolute_vals = True

def get_data() -> pd.DataFrame:
    with engine.begin() as conn:
        dataframe = pd.read_sql_table("training_data", conn).drop(columns=["index"])
    dataframe["date"] = dataframe["upload_time"].dt.date
    dataframe["count"] = 1
    dataframe["total"] = 1
    return dataframe

def set_optional_lists() -> tuple[list,str]:
    group_list = ["user", "date"]
    if view_move_types:
        group_list += ["correct_move"]
    if view_training_types:
        group_list += ["training_type"]
    if view_absolute_vals:
        y_column = "count"
    else:
        y_column = "percent"
    return group_list,y_column

def transform_data(dataframe:pd.DataFrame,group_list:list) -> pd.DataFrame:
    df_g1 = dataframe.groupby(group_list + ["was_correct"], as_index=False)["count"].count()
    df_g2 = dataframe.groupby(group_list, as_index=False)["total"].count()
    df_g = df_g1.merge(df_g2, on=group_list, how="inner").reset_index(drop=True)
    return df_g

def plot_figure(dataframe:pd.DataFrame,data_col:str) -> go.Figure:
    fig = go.Figure()
    legend_dict = dict.fromkeys(dataframe.was_correct.unique(), True)
    if view_move_types:
        legend_dict_move = dict.fromkeys(dataframe.correct_move.unique(), True)
    for val in dataframe.was_correct.unique():
        df_f = dataframe.loc[dataframe.was_correct == val, :]
        if view_move_types:
            for typ in df_f.correct_move.unique():
                df_p = df_f.loc[df_f.correct_move == typ]
                df_p.loc[:, "percent"] = df_f.loc[:, "count"] / df_f.loc[:, "total"]
                fig.add_trace(
                    go.Bar(
                        x=df_p["date"],
                        y=df_p[data_col],
                        marker={"color":COLOR_DICT[typ]},
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
                    marker={"color":COLOR_DICT[f"{val}"]},
                    legendgroup=f"{val}",
                    showlegend=legend_dict[val],
                )
            )
            legend_dict[val] = False
    return fig

def main_plot() -> go.Figure:
    dataframe = get_data()
    l1,c1 = set_optional_lists()
    dataframe = transform_data(dataframe,l1)
    fig = plot_figure(dataframe,c1)
    return fig