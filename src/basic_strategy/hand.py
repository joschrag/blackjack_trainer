"""This script contains classes to represent blackjack objects."""

CARD_VALS: dict = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}
SUITS: set = {"s", "h", "c", "d"}
SUIT_UNICODE: dict = {
    "s": 0x1F0A0,
    "h": 0x1F0B0,
    "d": 0x1F0C0,
    "c": 0x1F0D0,
}
RANK_UNICODE: dict = {
    "A": 0x1,
    "2": 0x2,
    "3": 0x3,
    "4": 0x4,
    "5": 0x5,
    "6": 0x6,
    "7": 0x7,
    "8": 0x8,
    "9": 0x9,
    "T": 0xA,
    "J": 0xB,
    "Q": 0xD,
    "K": 0xE,
}


class Card:
    """Class to represent a single card.

    Raises:
        KeyError: invalid card string
    """

    suit: str
    rank: str
    value: int
    unicode_front: str
    unicode_back: str = chr(0x1F0A0)
    face_up: bool

    def __init__(self, suit: str, rank: str, face_up: bool = True) -> None:
        """Initialize the card class.

        Args:
            suit (str): card suit
            rank (str): card rank
            face_up (bool, optional): is the card visible?. Defaults to True.
        """
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALS[rank]
        self.face_up = face_up
        self.unicode_front = chr(SUIT_UNICODE[suit] + RANK_UNICODE[rank])
        self.unicode = self.display_card()

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            str: card string
        """
        return f"<{self.rank}{self.suit}>"

    def __repr__(self) -> str:
        """Return string representation.

        Returns:
            str: card string
        """
        return f"<{self.rank}{self.suit}>"

    def display_card(self) -> str:
        """Display the card as unicode.

        Returns:
            str: card as unicode
        """
        return self.unicode_front if self.face_up else self.unicode_back

    def turn_card(self) -> None:
        """Flip the card over."""
        self.face_up = not self.face_up
        self.unicode = self.display_card()

    @staticmethod
    def from_string(card_str: str, face_up: bool = True) -> "Card":
        """Create a Card instance from a valid string.

        Args:
            card_str (str): card string (Examples: 8d, As, 2h,...)
            face_up (bool, optional): Is the card face up?. Defaults to True.

        Raises:
            KeyError: Invalid card string.

        Returns:
            Card: Class instance
        """
        if card_str[0] in CARD_VALS and card_str[1] in SUITS:
            return Card(card_str[1], card_str[0], face_up)
        raise KeyError(f"'{card_str}' is not a valid card string")


class Hand:
    """Class to represent a blackjack hand."""

    cards: list[Card]

    def __init__(self, cards: list[Card]) -> None:
        """Initialize a Hand object.

        Args:
            cards (list[Card]): Cards present in hand
        """
        self.cards = cards
        self.sorted_cards = sorted(cards, key=lambda c: CARD_VALS[c.rank])
        if len(cards) == 2 and cards[0].value == cards[1].value:
            self.is_pair = True
        else:
            self.is_pair = False
        self.is_hard_value = not (self.is_pair or any([card.rank == "A" for card in self.cards]))
        self.value = self.compute_value()
        self.rank_str = [card.rank for card in self.cards]
        self.card_str = "".join([f"{card.rank}{card.suit}" for card in self.cards])

    def compute_value(self) -> int:
        """Compute the hand value.

        Returns:
            int: hand value
        """
        naive_val = sum([CARD_VALS[card.rank] for card in self.cards])
        aces = [card for card in self.cards if card.rank == "A"]
        if aces and naive_val > 21:
            val = sum([CARD_VALS[card.rank] for card in self.sorted_cards[: -len(aces)]])
            if 21 - val > 11:
                return val + 11 + len(aces) - 1
            return val + len(aces)
        return naive_val

    @staticmethod
    def from_string(hands: str | list, face_up: list[bool] | str | list[str] = "") -> "Hand":
        """Create a hand from a card string.

        Args:
            hands (str | list): one or multiple chained card strings
            face_up (list[bool] | str | list[str], optional): Is each card face up? Defaults to "".

        Returns:
            Hand: Class instance
        """
        face_up = face_up if face_up else [True] * (len(hands) // 2)
        if isinstance(hands, str):
            hands = [hands[0 + i : 2 + i] for i in range(0, len(hands), 2)]  # noqa: E203
        if isinstance(face_up, str):
            face_up = list(face_up)
        face_bool = map(bool, map(int, face_up))
        cards = [Card.from_string(card, up) for card, up in zip(hands, face_bool)]
        return Hand(cards)
