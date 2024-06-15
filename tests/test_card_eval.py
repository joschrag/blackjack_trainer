import pytest

from basic_strategy import card_eval as bs
from basic_strategy.hand import Card, Hand

sur_list = [(16, 9), (16, 10), (16, 11), (15, 10)]
SUIT = "s"


@pytest.mark.parametrize(
    "card1", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
@pytest.mark.parametrize(
    "card2", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
@pytest.mark.parametrize(
    "dealer_value", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
def test_can_surr(card1: str, card2: str, dealer_value: str):
    hand = Hand([Card(SUIT, card1), Card(SUIT, card2)])
    dealer = Card(SUIT, dealer_value)
    res = bs.can_surrender(hand, dealer)
    if (hand.value, dealer.value) in sur_list:
        assert res
    else:
        assert not res


das_list = [(6, 2), (4, 5), (4, 6), (3, 2), (3, 3), (2, 3), (2, 2)]


@pytest.mark.parametrize(
    "card1", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
@pytest.mark.parametrize(
    "dealer_value", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
def test_can_split(card1: str, dealer_value: str):
    dealer = Card(SUIT, dealer_value)
    split_dict = {
        11: True,
        10: False,
        5: False,
        8: True,
        9: dealer.value not in [7, 10, 11],
        7: dealer.value < 8,
        6: 2 < dealer.value < 7,
        4: False,
        3: 3 < dealer.value < 8,
        2: 3 < dealer.value < 8,
    }
    hand = Hand([Card(SUIT, card1), Card(SUIT, card1)])
    res = bs.should_split(hand, dealer)
    if (hand.cards[0].value, dealer.value) in das_list:
        assert res == "das"
    elif split_dict[hand.cards[0].value]:
        assert res == "spl"
    else:
        assert res is None


double_list_soft = [
    (6, 3),
    (6, 4),
    (6, 5),
    (6, 6),
    (5, 4),
    (5, 5),
    (5, 6),
    (4, 4),
    (4, 5),
    (4, 6),
    (3, 5),
    (3, 6),
    (2, 5),
    (2, 6),
]
double_stand_list = [
    (8, 6),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (7, 6),
]
stand_list_soft = [
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 4),
    (10, 5),
    (10, 6),
    (10, 7),
    (10, 8),
    (10, 9),
    (10, 10),
    (10, 11),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
    (9, 6),
    (9, 7),
    (9, 8),
    (9, 9),
    (9, 10),
    (9, 11),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
    (8, 5),
    (8, 7),
    (8, 8),
    (8, 9),
    (8, 10),
    (8, 11),
    (7, 7),
    (7, 8),
]


@pytest.mark.parametrize(
    "card2", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
)
@pytest.mark.parametrize(
    "dealer_value", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
def test_soft_double(card2: str, dealer_value: str):
    hand = Hand([Card(SUIT, "A"), Card(SUIT, card2)])
    dealer = Card(SUIT, dealer_value)
    res = bs.should_double(hand, dealer)
    if (hand.cards[0].value, dealer.value) in double_list_soft:
        assert res == "d"
    elif (hand.cards[0].value, dealer.value) in double_stand_list:
        assert res == "ds"
    elif (hand.cards[0].value, dealer.value) in stand_list_soft:
        assert res == "s"
    else:
        assert res == "h"


double_list_hard = [
    (11, 1),
    (11, 2),
    (11, 3),
    (11, 4),
    (11, 5),
    (11, 6),
    (11, 7),
    (11, 8),
    (11, 9),
    (11, 10),
    (11, 11),
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 4),
    (10, 5),
    (10, 6),
    (10, 7),
    (10, 8),
    (10, 9),
    (9, 3),
    (9, 4),
    (9, 5),
    (9, 6),
]

stand_list_hard = [
    (17, 1),
    (17, 2),
    (17, 3),
    (17, 4),
    (17, 5),
    (17, 6),
    (17, 7),
    (17, 8),
    (17, 9),
    (17, 10),
    (17, 11),
    (16, 1),
    (16, 2),
    (16, 3),
    (16, 4),
    (16, 5),
    (16, 6),
    (15, 1),
    (15, 2),
    (15, 3),
    (15, 4),
    (15, 5),
    (15, 6),
    (14, 1),
    (14, 2),
    (14, 3),
    (14, 4),
    (14, 5),
    (14, 6),
    (13, 1),
    (13, 2),
    (13, 3),
    (13, 4),
    (13, 5),
    (13, 6),
    (12, 4),
    (12, 5),
    (12, 6),
]


@pytest.mark.parametrize(
    "card1", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
)
@pytest.mark.parametrize(
    "card2", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
)
@pytest.mark.parametrize(
    "dealer_value", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
)
def test_hard_double(card1: str, card2: str, dealer_value: str):
    hand = Hand([Card(SUIT, card1), Card(SUIT, card2)])
    dealer = Card(SUIT, dealer_value)
    res = bs.should_double(hand, dealer)
    if hand.value > 17:
        assert res == "s"
    elif (hand.value, dealer.value) in double_list_hard:
        assert res == "d"
    elif (hand.value, dealer.value) in stand_list_hard:
        assert res == "s"
    else:
        assert res == "h"
