"""Test game callback funtionality."""

from collections import Counter
from contextvars import copy_context

import pytest
from dash._callback_context import context_value

from src.app import game_callbacks as gc
from src.basic_strategy.card_eval import card_eval
from src.basic_strategy.hand import Hand


@pytest.mark.parametrize("n_clicks", list(range(0, 10**4, 10**3)))
@pytest.mark.parametrize("mode", ["split", "soft", "hard", "basic"])
@pytest.mark.parametrize(
    "card_data",
    [[], [{"owner": 0, "hands": "Kc9h", "face_up": "10"}, {"owner": 1, "hands": "4sJc", "face_up": "11"}]],
)
def test_cb_deal_and_save_cards(n_clicks: int, mode: str, card_data: list) -> None:
    html_cards, data = gc.deal_and_save_cards(n_clicks, mode, card_data, "test_user")
    assert isinstance(html_cards, list)
    if n_clicks == 0:
        assert data == card_data
    else:
        assert len(data) == 2
        assert Counter(data[0].keys()) == Counter(data[1].keys())


@pytest.mark.parametrize("btn_id", ["s", "d", "ds", "spl", "sur", "das", "h"])
@pytest.mark.parametrize("mode", ["basic"])
@pytest.mark.parametrize("dealer", [{"hands": "Kc9h", "face_up": "10"}])
@pytest.mark.parametrize("player", [{"hands": "Kc9h", "face_up": "11"}])
def test_cb_eval_action(btn_id: str, mode: str, dealer: dict, player: dict) -> None:
    def run_callback() -> list:
        context_value.set({"triggered_inputs": [{"prop_id": f"{btn_id}.n_clicks"}]})
        return gc.eval_action(
            [],
            1,
            [{"owner": 0, **dealer}, {"owner": 1, **player}],
            "test_user",
            mode,
        )

    ctx = copy_context()
    output = ctx.run(run_callback)
    hand = Hand.from_string(**player)
    dealer_hand = Hand.from_string(**dealer)
    res = card_eval(hand, dealer_hand.cards[0], mode)
    assert f"({res})" in output[0].children[0]
