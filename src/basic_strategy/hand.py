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
    suit: str
    rank: str
    value: int
    unicode_front: str
    unicode_back: str = chr(0x1F0A0)
    face_up: bool

    def __init__(self, suit: str, rank: str, face_up: bool = True) -> None:
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALS[rank]
        self.face_up = face_up
        self.unicode_front = chr(SUIT_UNICODE[suit] + RANK_UNICODE[rank])
        self.unicode = self.display_card()

    def __str__(self) -> str:
        return f"<{self.rank}{self.suit}>"

    def __repr__(self) -> str:
        return f"<{self.rank}{self.suit}>"

    def display_card(self) -> str:
        return self.unicode_front if self.face_up else self.unicode_back

    def turn_card(self) -> None:
        self.face_up = not self.face_up
        self.unicode = self.display_card()


class Hand:
    cards: list[Card]

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.sorted_cards = sorted(cards, key=lambda c: CARD_VALS[c.rank])
        self.value = self.compute_value()
        self.card_str = [card.rank for card in self.cards]

    def compute_value(self) -> int:
        naive_val = sum([CARD_VALS[card.rank] for card in self.cards])
        aces = [card for card in self.cards if card.rank == "A"]
        if aces and naive_val > 21:
            val = sum([CARD_VALS[card.rank] for card in self.sorted_cards[: -len(aces)]])
            if 21 - val > 11:
                return val + 11 + len(aces) - 1
            return val + len(aces)
        return naive_val
