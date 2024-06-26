"""This script contains functions to evaluate a blackjack hand."""

from typing import Optional

from src.basic_strategy.hand import Card, Hand


def can_surrender(hand: Hand, dealer: Card) -> bool:
    """Determine if the player should surrender.

    Args:
        hand (Hand): player cards
        dealer (Card): dealer cards

    Returns:
        bool: should surrender?
    """
    if hand.value == 16 and (9 <= dealer.value <= 11):
        return True
    if hand.value == 15 and dealer.value == 10:
        return True
    return False


def should_split(hand: Hand, dealer: Card) -> Optional[str]:
    """Determine if the player should split.

    Args:
        hand (Hand): player cards
        dealer (Card): dealer cards

    Returns:
        Optional[str]: None if player shouldnt split, "spl" if player should split, "das" if it depends on the rules.
    """
    if hand.cards[0].value != hand.cards[1].value:
        return None
    if hand.cards[0].value == hand.cards[1].value == 11 or hand.cards[0].value == hand.cards[1].value == 8:
        return "spl"
    if hand.cards[0].value == hand.cards[1].value == 10 or hand.cards[0].value == hand.cards[1].value == 5:
        return None
    if hand.cards[0].value == hand.cards[1].value == 9:
        return "spl" if dealer.value not in [7, 10, 11] else None
    if hand.cards[0].value == hand.cards[1].value == 7:
        return "spl" if dealer.value <= 7 else None
    if hand.cards[0].value == hand.cards[1].value == 6:
        if dealer.value == 2:
            return "das"
        return "spl" if 2 < dealer.value < 7 else None
    if hand.cards[0].value == hand.cards[1].value == 4:
        return "das" if dealer.value in [5, 6] else None
    if hand.cards[0].value == hand.cards[1].value == 3 or hand.cards[0].value == hand.cards[1].value == 2:
        if dealer.value in [2, 3]:
            return "das"
        return "spl" if 3 < dealer.value <= 7 else None
    return None


def should_double(hand: Hand, dealer: Card) -> str:
    """Determine if the player should double.

    Args:
        hand (Hand): player cards
        dealer (Card): dealer cards

    Returns:
        str: optimal action ("s" stand, "h" hit, "d" double or hit,"ds" double or stand)
    """
    if "A" in hand.rank_str:
        if "9" in hand.rank_str:
            return "s"
        if "8" in hand.rank_str:
            return "ds" if dealer.value == 6 else "s"
        if "7" in hand.rank_str:
            if dealer.value < 7:
                return "ds"
            return "s" if dealer.value <= 8 else "h"
        if "6" in hand.rank_str:
            return "d" if 3 <= dealer.value < 7 else "h"
        if "5" in hand.rank_str or "4" in hand.rank_str:
            return "d" if 4 <= dealer.value < 7 else "h"
        if "3" in hand.rank_str or "2" in hand.rank_str:
            return "d" if 5 <= dealer.value < 7 else "h"
    if hand.value >= 17:
        return "s"
    if 13 <= hand.value <= 16:
        return "s" if dealer.value <= 6 else "h"
    if hand.value == 12:
        return "s" if 4 <= dealer.value <= 6 else "h"
    if hand.value == 11:
        return "d"
    if hand.value == 10:
        return "d" if dealer.value <= 9 else "h"
    if hand.value == 9:
        return "d" if 3 <= dealer.value <= 6 else "h"
    if hand.value == 8:
        return "h"
    if hand.value < 8:
        return "h"
    return "o"


def card_eval(hand: Hand, dealer: Card, mode: str) -> str:
    """Completely evaluate a blackjack hand using basic strategy.

    Args:
        hand (Hand): player hand
        dealer (Card): dealer upcard
        mode (str): evaluation mode

    Returns:
        str: optimal choice
    """
    if can_surrender(hand, dealer):
        return "sur"
    if mode not in ["soft", "hard"]:
        if s := should_split(hand, dealer):
            return s
    return should_double(hand, dealer)
