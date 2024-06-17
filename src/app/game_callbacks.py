import datetime

import pandas as pd
from dash import Input, Output, State, callback, ctx, html

from src import engine
from src.basic_strategy.card_eval import card_eval
from src.basic_strategy.hand import Hand
from src.basic_strategy.mode_selector import deal_solo_cards

from .custom_html import html_hand


@callback(
    Output("bj-table", "children"),
    Output("cards_store", "data"),
    Input("start_btn", "n_clicks"),
    Input("gamemode_dd", "value"),
    State("cards_store", "data"),
    State("user_input", "value"),
    prevent_initial_callback=True,
)
def blackjack_game_loop(n_clicks: int, mode: str, data: list, username: str) -> tuple[list, list]:
    if username:
        if n_clicks:
            cards = deal_solo_cards(mode)
            cards[3].turn_card()
            player_hand = Hand(cards[0:2])
            dealer_hand = Hand(cards[2:4])
            card_df = pd.DataFrame(
                {
                    "owner": pd.Series([0, 1], dtype=pd.Int16Dtype()),
                    "hands": pd.Series([dealer_hand.card_str, player_hand.card_str], dtype=pd.StringDtype()),
                    "face_up": pd.Series(
                        [
                            "".join([str(int(card.face_up)) for card in dealer_hand.cards]),
                            "1" * len(player_hand.cards),
                        ],
                        dtype=pd.StringDtype(),
                    ),
                }
            )
            return [html_hand(dealer_hand, 0), html_hand(player_hand, 1)], card_df.to_dict("records")
        if data:
            card_df = pd.DataFrame(data)
            return [
                html_hand(Hand.from_string(row.hands, row.face_up), row.owner) for _, row in card_df.iterrows()
            ], data
    return [], []


MOVE_DICT = {
    "s": "stand (s)",
    "d": "double or hit (d)",
    "ds": "double or stand (ds)",
    "spl": "split (spl)",
    "sur": "surrender (sur)",
    "das": "double after split (das)",
    "h": "hit (h)",
}

COLOR_DICT = {
    "d": "rgba(0, 255, 0,",
    "das": "rgba(93, 39, 3,",
    "ds": "rgba(0, 204, 255,",
    "h": "rgba(255, 0, 0,",
    "s": "rgba(51, 51, 255,",
    "sur": "rgba(204, 0, 204,",
    "spl": "rgba(255, 102, 0,",
}


@callback(
    Output("correct_choice", "children"),
    inputs={
        "_": [
            Input("d", "n_clicks"),
            Input("ds", "n_clicks"),
            Input("das", "n_clicks"),
            Input("h", "n_clicks"),
            Input("s", "n_clicks"),
            Input("sur", "n_clicks"),
            Input("spl", "n_clicks"),
        ]
    },
    state={
        "data": State("cards_store", "data"),
        "user": State("user_input", "value"),
        "mode": State("gamemode_dd", "value"),
    },
)
def eval_action(_: list, data: list, user: str, mode: str):
    if data:
        chosen_action = ctx.triggered_id
        dataframe = pd.DataFrame(data)
        dealer, player = [Hand.from_string(row.hands, row.face_up) for _, row in dataframe.iterrows()]
        correct_action = card_eval(player, dealer.cards[0], "basic")
        df = pd.DataFrame(
            {
                "user": pd.Series([user], dtype=pd.StringDtype()),
                "training_type": pd.Series([mode], dtype=pd.StringDtype()),
                "was_correct": pd.Series([chosen_action == correct_action], dtype=pd.BooleanDtype()),
                "correct_move": pd.Series([correct_action], dtype=pd.StringDtype()),
                "guessed_move": pd.Series([chosen_action], dtype=pd.StringDtype()),
                "card1": pd.Series([player.cards[0].rank], dtype=pd.StringDtype()),
                "card2": pd.Series([player.cards[1].rank], dtype=pd.StringDtype()),
                "hand_value": pd.Series([player.value], dtype=pd.Int32Dtype()),
                "dealer_card": pd.Series([dealer.cards[1].value], dtype=pd.Int32Dtype()),
                "upload_time": pd.Series([datetime.datetime.now()], dtype="datetime64[ns]"),
            }
        )
        with engine.begin() as conn:
            df.to_sql("training_data", conn, if_exists="append")
        return [
            html.Button(
                [MOVE_DICT[correct_action]],
                disabled=True,
                className="gamebtn",
                style={
                    "borderColor": f"{COLOR_DICT[correct_action]}1)",
                    "backgroundColor": f"{COLOR_DICT[correct_action]}0.5)",
                },
            )
        ]
    return []
