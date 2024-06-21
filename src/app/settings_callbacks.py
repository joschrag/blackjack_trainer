import pandas as pd
import sqlalchemy as sa
from dash import Input, Output, State, callback, ctx

from src import SETTING_DTYPES, engine


@callback(
    Output("settings_store", "data"),
    Output("auto_deal", "checked"),
    Output("shoe_size_game", "value"),
    Output("das_game", "value"),
    Output("split_game", "checked"),
    Output("dealer_soft", "checked"),
    Output("split_num_game", "value"),
    Output("double_game", "value"),
    Output("shoe_size_train", "value"),
    Output("das_train", "value"),
    Input("auto_deal", "checked"),
    Input("shoe_size_game", "value"),
    Input("das_game", "value"),
    Input("split_num_game", "value"),
    Input("dealer_soft", "checked"),
    Input("split_game", "checked"),
    Input("double_game", "value"),
    Input("shoe_size_train", "value"),
    Input("das_train", "value"),
    State("settings_store", "data"),
)
def update_settings(
    auto_deal: bool,
    shoe_game: int,
    das_game: bool,
    split_aces: bool,
    deal_soft: bool,
    split_game: int,
    double_game: int,
    shoe_train: int,
    das_train: int,
    settings: list,
):
    table = sa.Table("settings", sa.MetaData(), autoload_with=engine)
    stmt = sa.select(table)
    if settings is None:
        with engine.begin() as conn:
            dataframe = pd.read_sql(
                stmt,
                conn,
            )
        settings = [{row[0]: dtype(row[1]) for row, dtype in zip(dataframe.to_dict("split")["data"], SETTING_DTYPES)}]
    if auto_deal is not None and ctx.triggered_id == "auto_deal":
        settings[0]["auto_deal"] = auto_deal
    if shoe_game is not None and ctx.triggered_id == "shoe_game":
        settings[0]["shoe_game"] = shoe_game
    if das_game is not None and ctx.triggered_id == "das_game":
        settings[0]["das_game"] = das_game
    if split_aces is not None and ctx.triggered_id == "split_aces":
        settings[0]["split_aces"] = split_aces
    if deal_soft is not None and ctx.triggered_id == "deal_soft":
        settings[0]["deal_soft"] = deal_soft
    if split_game is not None and ctx.triggered_id == "split_game":
        settings[0]["split_game"] = split_game
    if double_game is not None and ctx.triggered_id == "double_game":
        settings[0]["double_game"] = double_game
    if shoe_train is not None and ctx.triggered_id == "shoe_train":
        settings[0]["shoe_train"] = shoe_train
    if das_train is not None and ctx.triggered_id == "das_train":
        settings[0]["das_train"] = das_train

    df_upload = pd.DataFrame(
        {
            "settings": pd.Series(list(settings[0].keys()), dtype=pd.StringDtype()),
            "values": pd.Series(list(settings[0].values())),
        }
    )
    with engine.begin() as conn:
        df_upload.to_sql("settings", conn, index=False, if_exists="replace")

    return settings, *settings[0].values()
