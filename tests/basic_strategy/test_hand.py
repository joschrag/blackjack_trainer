import itertools
from collections import Counter

import pytest

from src.basic_strategy.hand import Card, Deck, Hand


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
    "cards,value,pair,hard",
    zip(
        [
            [Card("s", "4")],
            [Card("s", "4"), Card("d", "7"), Card("c", "K")],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [Card("s", "A"), Card("h", "Q"), Card("d", "A"), Card("s", "2")],
        ],
        [4, 21, 12, 16, 14],
        [False, False, True, False, False],
        [True, True, False, False, True],
    ),
)
def test_init_hand(cards: list[Card], value: int, pair: bool, hard: bool):
    hand = Hand(cards)
    assert hand.value == value
    assert hand.is_pair == pair
    assert hand.is_hard_value == hard


@pytest.mark.parametrize(
    ["hand_cards", "add_cards"],
    zip(
        [
            [],
            [Card("s", "4")],
            [Card("s", "4"), Card("d", "7"), Card("c", "K")],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [Card("s", "A"), Card("h", "Q"), Card("d", "A"), Card("s", "2")],
            [Card("s", "4")],
            [Card("s", "4"), Card("d", "7"), Card("c", "K")],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [],
        ],
        [
            [],
            [Card("s", "4")],
            [Card("s", "4"), Card("d", "7"), Card("c", "K")],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [Card("s", "4")],
            [],
            [Card("s", "A"), Card("s", "A")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
            [Card("s", "A"), Card("h", "Q"), Card("d", "A"), Card("s", "2")],
            [Card("s", "A"), Card("s", "4"), Card("s", "A")],
        ],
    ),
)
def test_add_card(hand_cards: list[Card], add_cards: list[Card]) -> None:
    hand = Hand(hand_cards)
    hand.add_cards(add_cards)
    assert hand == Hand(hand_cards + add_cards)


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


@pytest.mark.parametrize("suits", [["h", "c", "s", "d"], ["h"], ["c", "s"]])
@pytest.mark.parametrize(
    "ranks",
    [
        ["J", "A"],
        ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
        ["2", "7", "8", "9", "T", "J", "Q", "K", "A"],
        ["2"],
    ],
)
def test_deck(suits: list[str], ranks: list[str]) -> None:
    deck_cards = [Card(s, r) for s, r in itertools.product(suits, ranks)]
    deck = Deck(deck_cards)
    assert deck.cards.size == deck.cur_cards.size == len(deck_cards)


@pytest.mark.parametrize("suits", [["h", "c", "s", "d"], ["h"], ["c", "s"]])
@pytest.mark.parametrize(
    "ranks",
    [
        ["J", "A"],
        ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
        ["2", "7", "8", "9", "T", "J", "Q", "K", "A"],
        ["2"],
    ],
)
@pytest.mark.parametrize("num_cards", [1, 5, 52, 245, 12])
def test_deck_deal_cards(suits: list[str], ranks: list[str], num_cards: int) -> None:
    deck_cards = [Card(s, r) for s, r in itertools.product(suits, ranks)]
    deck = Deck(deck_cards)
    old_cards = deck.cur_cards
    hand = deck.draw_to_hand(num_cards=num_cards)
    max_comp_ind = min(old_cards.size, num_cards)
    assert Counter(hand.cards[:max_comp_ind]) == Counter(old_cards[:max_comp_ind])
