import pytest

from basic_strategy import mode_selector
from basic_strategy.hand import Card


@pytest.mark.repeat(10**3)
@pytest.mark.parametrize("mode", ["basic", "soft", "hard", "split"])
def test_mode_selector(mode: str):
    cards = mode_selector.deal_cards(mode)
    assert isinstance(cards, (list, Card))
    if mode == "soft":
        assert cards[0].rank == "A" and 2 <= cards[1].value <= 9
    elif mode == "split":
        assert cards[0].rank == cards[1].rank
    elif mode == "hard":
        assert cards[0].rank != "A" and cards[1].rank != "A"
