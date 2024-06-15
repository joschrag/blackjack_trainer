from collections import Counter

import pytest

from basic_strategy.hand import Card, Hand


@pytest.mark.parametrize(
    "cards,value",
    zip(
        [
            [Card("s", "4")],
            [Card("s", "4"), Card("d", "7"), Card("c", "K")],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [Card("s", "A"), Card("h", "Q"), Card("d", "A"), Card("s", "2")],
        ],
        [4, 21, 12, 16, 14],
    ),
)
def test_init_hand(cards: list[Card], value: int):
    hand = Hand(cards)
    # assert Counter(hand.cards) == Counter(cards)
    assert hand.value == value
