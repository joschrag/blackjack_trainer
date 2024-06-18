import pytest

from src.basic_strategy.hand import Card, Hand


@pytest.mark.parametrize(
    "cards,value",
    zip(
        [
            "4s",
            "4s7dKc",
            "AsAd",
            "As4sAd",
            "AsQhAd2h",
        ],
        [4, 21, 12, 16, 14],
    ),
)
def test_hand_from_string(cards: str, value: int):
    hand = Hand.from_string(cards)
    assert hand.value == value


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
    assert hand.value == value


@pytest.mark.parametrize(
    "rank,value",
    zip(
        ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11],
    ),
)
@pytest.mark.parametrize("suit", ["s", "h", "c", "d"])
def test_init_card(rank: str, suit: str, value: int):
    card = Card(suit, rank)
    assert card.value == value


@pytest.mark.parametrize(
    "rank,value",
    zip(
        ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11],
    ),
)
@pytest.mark.parametrize("suit", ["s", "h", "c", "d"])
def test_card_from_string(rank: str, suit: str, value: int):
    card_str = f"{rank}{suit}"
    card = Card.from_string(card_str)
    assert card.rank == rank
    assert card.suit == suit
