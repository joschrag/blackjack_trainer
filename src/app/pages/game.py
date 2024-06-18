"""This script defines the page layout for the game page."""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from src.app import game_callbacks  # noqa: F401

dash.register_page(
    __name__,
    path="/",
    name="Blackjack Trainer",
    title="Blackjack Trainer",
    description="Landing page.",
)

gamemode_dd = dcc.Dropdown(
    ["basic", "hard", "soft", "split"],
    "basic",
    clearable=False,
    id="gamemode_dd",
    persistence=True,
    persistence_type="session",
)
user_input = dcc.Input(
    type="text", placeholder="Enter your name", id="user_input", persistence=True, persistence_type="session"
)
start_button = html.Button("Deal Cards", id="start_btn", className="gamebtn")
correct_choice = html.Div(id="correct_choice")

double_button = html.Button("double or hit (d)", id="d", className="gamebtn")
surrender_button = html.Button("surrender (sur)", id="sur", className="gamebtn")
doublestand_button = html.Button("double or stand (ds)", id="ds", className="gamebtn")
hit_button = html.Button("hit (h)", id="h", className="gamebtn")
stand_button = html.Button("stand (s)", id="s", className="gamebtn")
das_button = html.Button("double after split (das)", id="das", className="gamebtn")
split_button = html.Button("split (spl)", id="spl", className="gamebtn")


layout: list = [
    dbc.Row(
        [
            dbc.Col(user_input, width=2),
            dbc.Col(gamemode_dd, width=2),
            dbc.Col(correct_choice, width=2),
            dbc.Col(start_button, width=2),
        ],
        id="button_row",
    ),
    html.Div([], id="bj-table"),
    dbc.Row(
        dbc.Col(
            [surrender_button, doublestand_button, stand_button, hit_button, double_button, split_button, das_button],
            id="button_row",
        ),
    ),
]
