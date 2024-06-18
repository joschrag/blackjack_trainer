"""This script contains custom html components used in the app."""

from dash import html

from src.basic_strategy.hand import Hand

COLOUR_DICT = {"h": "red", "d": "red", "c": "black", "s": "black"}
CSS_CLASS_DICT = {0: "dealer", 1: "player"}


def html_hand(hand: Hand, player: int) -> html.Span:
    """Create a thml repr of the hand class.

    Args:
        hand (Hand): Hand object to create in html
        player (int): playernumber controlling the position.

    Returns:
        html.Span: html repr of hand object
    """
    web_hand = html.Span(
        [
            html.Span(
                card.unicode,
                className=COLOUR_DICT[card.suit] if card.face_up else "blue",  # type:ignore[attr-defined]
            )
            for card in hand.cards
        ],
        className=f"hand {CSS_CLASS_DICT[player]}",
    )
    return web_hand
