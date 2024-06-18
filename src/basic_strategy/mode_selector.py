"""This script contains functions to deal cards and create card decks."""

import itertools
import random

from src.basic_strategy.hand import Card

SUITS = ["h", "c", "s", "d"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def deal_solo_cards(mode: str) -> list[Card]:
    """Deal cards to a single player and the dealer.

    Args:
        mode (str): selected mode, influences which deck is created.

    Returns:
        list[Card]: dealt cards
    """
    deck = [Card(s, r) for s, r in itertools.product(SUITS, RANKS)]
    if mode == "split":
        cards = random.sample(deck, k=3)
        return [cards[0], *cards]
    if mode == "soft":
        ranks = RANKS[:-5]
        deck = [Card(s, r) for s, r in itertools.product(SUITS, ranks)]
        cards = random.sample(deck, k=3)
        return [Card("s", "A"), *cards]
    if mode == "hard":
        ranks = RANKS[:-1]
        deck = [Card(s, r) for s, r in itertools.product(SUITS, ranks)]
        cards = random.sample(deck, k=4)
        return cards
    cards = random.sample(deck, k=4)
    return cards
