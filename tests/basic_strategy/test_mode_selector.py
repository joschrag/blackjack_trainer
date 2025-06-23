"""Unit tests for the mode selector script."""

import pytest

from blackjack_trainer.blackjack import mode_selector
from blackjack_trainer.blackjack.hand import Card


@pytest.mark.repeat(10)
@pytest.mark.parametrize("mode", ["basic", "soft", "hard", "split"])
def test_mode_selector(mode: str) -> None:
    """Test that the dealt cards are matching the deal mode.
      Repeats 10 times per mode.

    Args:
        mode (str): deal mode
    """
    cards = mode_selector.deal_solo_cards(mode)
    assert isinstance(cards, (list, Card))
    if mode == "soft":
        assert cards[0].rank == "A" and 2 <= cards[1].value <= 9
    elif mode == "split":
        assert cards[0].rank == cards[1].rank
    elif mode == "hard":
        assert cards[0].rank != "A" and cards[1].rank != "A"
