import itertools
import random

from basic_strategy.hand import Card

SUITS = ["h", "c", "s", "d"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def deal_cards(mode: str) -> list[Card]:
    deck = [Card(s, r) for s, r in itertools.product(SUITS, RANKS)]
    if mode == "split":
        cards = random.sample(deck, k=2)
        return [cards[0], cards[0], cards[1]]
    if mode == "soft":
        ranks = RANKS[:-5]
        deck = [Card(s, r) for s, r in itertools.product(SUITS, ranks)]
        cards = random.sample(deck, k=2)
        return [Card("s", "A"), cards[0], cards[1]]
    if mode == "hard":
        ranks = RANKS[:-1]
        deck = [Card(s, r) for s, r in itertools.product(SUITS, ranks)]
        cards = random.sample(deck, k=3)
        return cards
    cards = random.sample(deck, k=3)
    return cards
