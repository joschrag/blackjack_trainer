"""Test game callback funtionality."""

from collections import Counter
from contextlib import nullcontext
from contextvars import copy_context

import dash
import pytest
from dash._callback_context import context_value
from dash._utils import AttributeDict

from blackjack_trainer.app import custom_html
from blackjack_trainer.app import game_callbacks as gc
from blackjack_trainer.blackjack.card_eval import hand_eval
from blackjack_trainer.blackjack.hand import Hand

# pylint: disable-next=import-error,unused-import
from tests.fixtures import setup_db  # noqa: F401


@pytest.mark.parametrize("tab", ["train", "game"])
@pytest.mark.parametrize("n_clicks", list(range(0, 10**4, 10**3)))
@pytest.mark.parametrize("mode", ["split", "soft", "hard", "basic"])
@pytest.mark.parametrize(
    "card_data",
    [[], [{"owner": 0, "hands": "Kc9h", "face_up": "10"}, {"owner": 1, "hands": "4sJc", "face_up": "11"}]],
)
# pylint: disable-next=too-many-arguments,too-many-positional-arguments,redefined-outer-name
def test_cb_deal_and_save_cards(n_clicks: int, mode: str, card_data: list, tab: str) -> None:
    """Test the deal and save cards callback.

    Args:
        n_clicks (int): number of btn clicks
        mode (str): deal mode
        card_data (list): current card data
        tab (str): chosen tab
    """
    if tab != "train":
        expected_error = pytest.raises(dash.exceptions.PreventUpdate)
    else:
        expected_error = nullcontext()
    with expected_error:
        data = gc.deal_and_save_cards_train(n_clicks, mode, card_data, "test_user", tab)
    if isinstance(expected_error, nullcontext):
        if n_clicks == 0:
            assert data == []
        else:
            assert len(data) == 2
            assert Counter(data[0].keys()) == Counter(data[1].keys())


@pytest.mark.parametrize("tab", ["train", "game"])
@pytest.mark.parametrize("btn_id", ["s", "d", "ds", "spl", "sur", "das", "h"])
@pytest.mark.parametrize("mode", ["basic"])
@pytest.mark.parametrize("dealer", [{"hands": "Kc9h", "face_up": "10"}])
@pytest.mark.parametrize("player", [{"hands": "Kc9h", "face_up": "11"}])
# pylint: disable-next=too-many-arguments,too-many-positional-arguments,redefined-outer-name
def test_cb_eval_action(
    setup_db, mocker, btn_id: str, mode: str, dealer: dict, player: dict, tab: str  # noqa: F811
) -> None:  # noqa:F811
    """Test the training hand evaluation callback.

    Args:
        setup_db : db setup fixture
        mocker : pytest mock fixture
        btn_id (str): pressed button
        mode (str): current deal mode
        dealer (dict): dealer cards
        player (dict): player cards
        tab (str): current tab
    """
    engine, _ = setup_db
    mocker.patch("blackjack_trainer.app.game_callbacks.engine", engine)

    def run_callback() -> tuple[list, list, list]:
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": f"{btn_id}.n_clicks"}]}))
        return gc.eval_action_train([], 1, [{"owner": 0, **dealer}, {"owner": 1, **player}], "test_user", mode, tab)

    ctx = copy_context()

    if tab != "train":
        expected_error = pytest.raises(dash.exceptions.PreventUpdate)
    else:
        expected_error = nullcontext()
    with expected_error:
        output = ctx.run(run_callback)
    hand = Hand.from_string(**player)
    dealer_hand = Hand.from_string(**dealer)
    res = hand_eval(hand, dealer_hand.cards[0])
    if isinstance(expected_error, nullcontext):
        assert f"({res})" in output[1][0].children[0]


@pytest.mark.parametrize(
    "trigger",
    ["cards_store_train", "cards_store_game"],
)
@pytest.mark.parametrize(
    "game_cards",
    [
        [{"owner": 0, "hands": "Kc9h", "face_up": "10"}, {"owner": 1, "hands": "Kc9h", "face_up": "11"}],
        [{"owner": 0, "hands": "Kc3h", "face_up": "00"}, {"owner": 1, "hands": "Kc2h", "face_up": "10"}],
    ],
)
@pytest.mark.parametrize(
    "train_cards",
    [
        [{"owner": 0, "hands": "Kc9h", "face_up": "10"}, {"owner": 1, "hands": "Kc3h", "face_up": "11"}],
        [{"owner": 0, "hands": "KcTh", "face_up": "00"}, {"owner": 1, "hands": "KcAh", "face_up": "01"}],
    ],
)
def test_display_cards(game_cards: list, train_cards: list, trigger: str) -> None:
    """Test displaying cards through callback.

    Args:
        game_cards (list): game cards to display
        train_cards (list): train cards to display
        trigger (str): current tab
    """

    def run_callback() -> tuple[list, list, list]:
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": f"{trigger}.data"}]}))
        return gc.display_cards(game_cards, train_cards)

    ctx = copy_context()
    output = ctx.run(run_callback)
    t_hands: list[dash.html.Span] = []
    g_hands: list[dash.html.Span] = []

    if trigger == "cards_store_train":
        t_hands = [
            custom_html.html_hand(Hand.from_string(hand.get("hands"), hand.get("face_up")), player)
            for player, hand in enumerate(train_cards)
        ]
        disp_hand = [el.children for el in output[1][0].children]
        t_hand_content = [el.children for el in t_hands[0].children]
        assert disp_hand == t_hand_content
    if trigger == "cards_store_game":
        g_hands = [
            custom_html.html_hand(Hand.from_string(hand.get("hands"), hand.get("face_up")), player)
            for player, hand in enumerate(game_cards)
        ]
        disp_hand = [el.children for el in output[0][0].children]
        g_hand_content = [el.children for el in g_hands[0].children]
        assert disp_hand == g_hand_content
