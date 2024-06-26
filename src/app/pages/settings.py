"""This script defines the page layout for the /settings page."""

import dash

dash.register_page(
    __name__,
    path="/settings",
    name="Blackjack Trainer Settings",
    title="Blackjack Trainer Settings",
    description="Settings page.",
)
layout: list = []
