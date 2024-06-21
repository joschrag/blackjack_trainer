"""This script defines the dash app and its template layout."""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from . import game_callbacks, settings_callbacks, ui_callbacks  # noqa: F401

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.MATERIA, "assets/style.css"],
)
nav_link_style = {
    "margin": "1em 1em",
    "text-align": "center",
    "padding": "0.5em 2em",
}

navbar = dbc.Navbar(
    [
        # Use row and col to control vertical alignment of logo / brand
        dbc.Nav(
            [
                dbc.NavLink("Game", href="/", active="exact", style=nav_link_style),
                dbc.NavLink(
                    "Dashboard",
                    href="/dashboard",
                    active="exact",
                    style=nav_link_style,
                ),
                dbc.NavLink(
                    "Settings",
                    href="/settings",
                    active="exact",
                    style=nav_link_style,
                ),
            ],
            vertical=False,
            pills=True,
        )
    ],
    style={
        "padding-left": "10em",
        "padding-bottom": "3em",
        "border": "none",
        "width": "auto",
        "box-shadow": "none",
        "background-color": "none",
    },
)

app.layout = dbc.Container(
    children=[
        navbar,
        dbc.Row(html.Div(dash.page_container)),
        dcc.Interval(id="1_min", interval=1000 * 60),
        dcc.Interval(id="10_min", interval=1000 * 10 * 60),
        dcc.Store("data_store", storage_type="session"),
        dcc.Store("cards_store_train", storage_type="session"),
        dcc.Store("cards_store_game", storage_type="session"),
        dcc.Store("settings_store", storage_type="session"),
    ],
    className="dbc",
    fluid=True,
)
