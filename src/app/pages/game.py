import dash
from dash import html

dash.register_page(
    __name__,
    path="/",
    name="Blackjack Trainer",
    title="Blackjack Trainer",
    description="Landing page.",
)


layout: list = [html.Div([], id="bj-table")]
