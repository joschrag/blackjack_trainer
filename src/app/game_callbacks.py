"""This script contains the callbacks used in the app gameplay loop."""

import datetime
import itertools
import logging
import math

import dash
import dash_mantine_components as dmc
import pandas as pd
import sqlalchemy as sa
from dash import Input, Output, State, callback, ctx, html
from dash_iconify import DashIconify

from src import TABLE_DTYPES, engine
from src.basic_strategy.card_eval import hand_eval
from src.basic_strategy.hand import Card, Deck, Hand
from src.basic_strategy.mode_selector import deal_solo_cards

from .custom_html import html_hand

logger = logging.getLogger(__name__)


@callback(
    Output("chips_display", "children"),
    Output("chips_store", "data"),
    Input("user_btn", "n_clicks"),
    State("user_input", "value"),
)
def display_player_chips(n_clicks: int, user: str) -> tuple[dmc.Text, list]:
    table = sa.Table("player_chips", sa.MetaData(), autoload_with=engine)
    stmt = sa.select(table)
    with engine.begin() as conn:
        chips_df = pd.read_sql(stmt, conn, index_col="index")
    logger.info("Loaded chips data: %s rows %s cols", *chips_df.shape)
    current_chips = 0
    chips_store = []
    if n_clicks:
        if not user:
            raise dash.exceptions.PreventUpdate()
        if chips_df is not None:
            chips_df = pd.DataFrame(chips_df)
        if chips_df is None or user not in chips_df.user.unique():
            # User hasnt played before
            new_player_df = pd.DataFrame(
                {
                    "user": pd.Series([user], dtype=pd.StringDtype()),
                    "chips": pd.Series([1000], dtype=pd.Int64Dtype()),
                    "upload_time": pd.Series([datetime.datetime.now()], dtype="datetime64[ns]"),
                }
            )
            with engine.begin() as conn:
                new_player_df.to_sql("player_chips", conn, if_exists="append", index=False)
            chips_df = pd.concat([chips_df, new_player_df]) if not chips_df.empty else new_player_df
        current_chips = chips_df.loc[chips_df.user == user, "chips"].iloc[-1]
        chips_store = chips_df.to_dict("records")
    return dmc.Text([current_chips, DashIconify(icon="material-symbols:monetization-on", width=50)]), chips_store


@callback(
    Output("cards_store_train", "data", allow_duplicate=True),
    Input("start_btn", "n_clicks"),
    Input("gamemode_dd", "value"),
    State("cards_store_train", "data"),
    State("user_input", "value"),
    State("bj-tabs", "value"),
    prevent_initial_call="initial_duplicate",
)
def deal_and_save_cards_train(n_clicks: int, mode: str, data: list, username: str, tab: str) -> list:
    """Deal cards and saves them in a store object.

    Args:
        n_clicks (int): click number of the deal button
        mode (str): training mode (what deck is used?)
        data (list): current card data
        username (str): current user

    Returns:
        tuple[list, list]: html card objects, updated card data
    """
    if tab != "train":
        raise dash.exceptions.PreventUpdate
    if username:
        if n_clicks:
            card_df = deal_cards(mode)
            return card_df.to_dict("records")
    return []


@callback(
    Output("cards_store_game", "data", allow_duplicate=True),
    Output("bet_chips", "disabled"),
    Input("start_btn", "n_clicks"),
    State("cards_store_game", "data"),
    State("user_input", "value"),
    State("bj-tabs", "value"),
    State("bet_chips", "value"),
    prevent_initial_call="initial_duplicate",
)
def deal_and_save_cards_game(n_clicks: int, data: list, username: str, tab: str, bet_chips: int) -> tuple[list, bool]:
    """Deal cards and saves them in a store object.

    Args:
        n_clicks (int): click number of the deal button
        data (list): current card data
        username (str): current user

    Returns:
        tuple[list, list]: html card objects, updated card data
    """
    if tab != "game":
        raise dash.exceptions.PreventUpdate
    if username and bet_chips:
        if n_clicks:
            card_df = deal_cards("basic")
            return card_df.to_dict("records"), True
    return [], False


def deal_cards(mode) -> pd.DataFrame:
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

    return card_df


@callback(
    Output("bjt-game", "children"),
    Output("bjt-train", "children"),
    Input("cards_store_game", "data"),
    Input("cards_store_train", "data"),
)
def display_cards(game_cards: list, train_cards: list) -> tuple[list, list]:
    game_hand = []
    train_hand = []
    if game_cards and ctx.triggered_id == "cards_store_game":
        card_df = pd.DataFrame(game_cards)
        logger.info("Game cards updated")
        game_hand = [html_hand(Hand.from_string(row.hands, row.face_up), row.owner) for _, row in card_df.iterrows()]
    if train_cards and ctx.triggered_id == "cards_store_train":
        card_df = pd.DataFrame(train_cards)
        logger.info("Train cards updated")
        train_hand = [html_hand(Hand.from_string(row.hands, row.face_up), row.owner) for _, row in card_df.iterrows()]
    return game_hand, train_hand


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

RANKS: set = {
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
}
SUITS: set = {"s", "h", "c", "d"}


@callback(
    Output("cards_store_game", "data", allow_duplicate=True),
    Output("game_store", "data", allow_duplicate=True),
    Output("correct_choice", "children", allow_duplicate=True),
    inputs={
        "_": [
            Input("d", "n_clicks"),
            Input("ds", "n_clicks"),
            Input("das", "n_clicks"),
            Input("h", "n_clicks"),
            Input("s", "n_clicks"),
            Input("sur", "n_clicks"),
            Input("spl", "n_clicks"),
        ],
        "n_clicks": Input("start_btn", "n_clicks"),
    },
    state={
        "data_train": State("cards_store_train", "data"),
        "data_game": State("cards_store_game", "data"),
        "user": State("user_input", "value"),
        "mode": State("gamemode_dd", "value"),
        "tab": State("bj-tabs", "value"),
        "game_data": State("game_store", "data"),
        "deck_data": State("deck_store", "data"),
        "chips_data": State("chips_store", "data"),
        "bet_chips": State("bet_chips", "value"),
    },
    prevent_initial_call="initial_duplicate",
)
def eval_action_game(
    _: list,
    n_clicks: int,
    data_train: list,
    data_game: list,
    user: str,
    mode: str,
    tab: str,
    game_data: list,
    deck_data: list,
    chips_data: list,
    bet_chips: int,
) -> tuple[list, int, list[html.Button]]:
    """Evaluate a chosen action against the basic strategy and display correct choice.

    Also writes choices to database.

    Args:
        _ (list): buttons of basic strategy choices
        n_clicks (int): click number of the deal button
        data (list): current card data
        user (str): current user
        mode (str): selected training mode (affects evaluation)

    Returns:
        list[html.Button]: correct choice
    """
    logger.info("Game action callback")
    if not ctx.triggered_id:
        return [], 0, []
    if ctx.triggered_id == "start_btn" and not n_clicks:
        return [], 0, []
    if tab != "game":
        raise dash.exceptions.PreventUpdate()
    deck_cards = [Card(s, r) for s, r in itertools.product(SUITS, RANKS)]
    if not deck_data:
        deck = Deck(deck_cards)
    else:
        cur_cards = [Card.from_string(card) for card in deck_data]
        deck = Deck(deck_cards, cur_cards)
    if data_game and chips_data:
        chosen_action = ctx.triggered_id
        dataframe = pd.DataFrame(data_game)
        chips_df = pd.DataFrame(chips_data)
        current_chips = chips_df.loc[chips_df.user == user, "chips"].iloc[-1]
        dealer_hand, player_hand = [Hand.from_string(row.hands, row.face_up) for _, row in dataframe.iterrows()]
        has_lost = False
        factor = 1.0
        if chosen_action == "h":
            player_hand = deck.draw_to_hand(player_hand, 1)
            if player_hand.value > 21:
                has_lost = True
            logger.info("Hit")
        elif chosen_action == "d":
            player_hand = deck.draw_to_hand(player_hand, 1)
            factor = 2.0

            if player_hand.value > 21:
                has_lost = True

            logger.info("Double")
        elif chosen_action == "s":
            logger.info("Stand")
        elif chosen_action == "sur":
            has_lost = True
            factor = 0.5
            logger.info("Surrender")
        elif chosen_action == "spl":
            logger.info("Split")
        else:
            logger.error("Illegal action!")
        owner_list = [0, 1]
        hands = [dealer_hand, player_hand]
        card_df = cards_to_data(owner_list, hands)
        if has_lost:
            player_credits = current_chips - math.ceil(factor * bet_chips)
            logger.info(player_credits)
        elif chosen_action not in ["h", "spl"]:
            dealer_hand.cards[1].turn_card()
            owner_list = [0, 1]
            hands = [dealer_hand, player_hand]
            card_df = cards_to_data(owner_list, hands)
            owner_list = [0, 1]
            hands = [dealer_hand, player_hand]
            card_df = cards_to_data(owner_list, hands)
            return card_df.to_dict("records"), 1, []
            # if dealer_hand.value > 21 or player_hand.value > dealer_hand.value:
            #     player_credits = current_chips + math.ceil(factor * bet_chips)
            # elif player_hand.value < dealer_hand.value:
            #     player_credits = current_chips - math.ceil(factor * bet_chips)
            # elif player_hand.value == dealer_hand.value:
            #     player_credits = current_chips
        owner_list = [0, 1]
        hands = [dealer_hand, player_hand]
        card_df = cards_to_data(owner_list, hands)
        return card_df.to_dict("records"), 2, []
    raise dash.exceptions.PreventUpdate()


def cards_to_data(owner_list, hands):
    card_df = pd.DataFrame(
        {
            "owner": pd.Series(owner_list, dtype=pd.Int16Dtype()),
            "hands": pd.Series([hand.card_str for hand in hands], dtype=pd.StringDtype()),
            "face_up": pd.Series(
                ["".join([str(int(card.face_up)) for card in hand.cards]) for hand in hands],
                dtype=pd.StringDtype(),
            ),
        }
    )

    return card_df


@callback(
    Output("cards_store_game", "data"),
    Output("game_store", "data"),
    Input("cards_store_game", "data"),
    State("game_store", "data"),
    State("deck_store", "data"),
    prevent_initial_call="initial_duplicate",
)
def dealer_turn(card_data: list, cur_turn: int, deck_data: list) -> tuple[list, int]:
    logger.info("Dealer turn callback")
    if card_data and cur_turn == 1:
        cur_cards = [Card.from_string(card) for card in deck_data]
        deck_cards = [Card(s, r) for s, r in itertools.product(SUITS, RANKS)]
        deck = Deck(deck_cards, cur_cards)
        card_df = pd.DataFrame(card_data)
        dealer_hand, player_hand = [Hand.from_string(row.hands, row.face_up) for _, row in card_df.iterrows()]
        if dealer_hand.value < 17:
            dealer_hand = deck.draw_to_hand(dealer_hand, 1)
            owner_list = [0, 1]
            hands = [dealer_hand, player_hand]
            card_df = cards_to_data(owner_list, hands)
            if dealer_hand.value > 17:
                cur_turn = 0
            else:
                cur_turn = 1
        else:
            cur_turn = 0
        return card_df.to_dict("records"), cur_turn
    raise dash.exceptions.PreventUpdate()


@callback(
    Output("cards_store_train", "data"),
    Output("correct_choice", "children"),
    Output("deck_store", "data"),
    inputs={
        "_": [
            Input("d", "n_clicks"),
            Input("ds", "n_clicks"),
            Input("das", "n_clicks"),
            Input("h", "n_clicks"),
            Input("s", "n_clicks"),
            Input("sur", "n_clicks"),
            Input("spl", "n_clicks"),
        ],
        "n_clicks": Input("start_btn", "n_clicks"),
    },
    state={
        "data_train": State("cards_store_train", "data"),
        "user": State("user_input", "value"),
        "mode": State("gamemode_dd", "value"),
        "tab": State("bj-tabs", "value"),
    },
    prevent_initial_call="initial_duplicate",
)
def eval_action_train(
    _: list,
    n_clicks: int,
    data_train: list,
    user: str,
    mode: str,
    tab: str,
) -> tuple[list[html.Button], list, list]:
    """Evaluate a chosen action against the basic strategy and display correct choice.

    Also writes choices to database.

    Args:
        _ (list): buttons of basic strategy choices
        n_clicks (int): click number of the deal button
        data (list): current card data
        user (str): current user
        mode (str): selected training mode (affects evaluation)

    Returns:
        list[html.Button]: correct choice
    """
    logger.info("Train action callback")
    if not ctx.triggered_id:
        return [], [], []
    if ctx.triggered_id == "start_btn" and not n_clicks:
        return [], [], []
    if tab != "train":
        raise dash.exceptions.PreventUpdate()

    if data_train:
        if ctx.triggered_id == "start_btn" and n_clicks:
            return [], [], []
        chosen_action = ctx.triggered_id
        dataframe = pd.DataFrame(data_train)
        dealer, player = [Hand.from_string(row.hands, row.face_up) for _, row in dataframe.iterrows()]
        correct_action = check_basic_strat(user, mode, chosen_action, dealer, player)
        return_btn = [
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
        logger.info("train callback finished")
        return data_train, return_btn, []
    return [], [], []


def check_basic_strat(user, mode, chosen_action, dealer, player):
    correct_action = hand_eval(player, dealer.cards[0])
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
        },
    ).astype(TABLE_DTYPES)
    with engine.begin() as conn:
        df.to_sql("training_data", conn, if_exists="append", index=False)
    return correct_action
