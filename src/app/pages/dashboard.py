import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

dash.register_page(
    __name__,
    path="/dashboard",
    name="Blackjack Trainer Dashboard",
    title="Blackjack Trainer Dashboard",
    description="Landing page.",
)
user_switch = dmc.Switch(
    "separate users",
    id="user_switch",
    size="md",
    radius="xl",
    color="ff0000",
    persistence=True,
    persistence_type="session",
)
mode_switch = dmc.Switch(
    "separate modes",
    id="mode_switch",
    size="md",
    radius="xl",
    color="ff0000",
    persistence=True,
    persistence_type="session",
)
move_switch = dmc.Switch(
    "separate moves",
    id="move_switch",
    size="md",
    radius="xl",
    color="ff0000",
    persistence=True,
    persistence_type="session",
)
abs_val_dd = dcc.Dropdown(
    ["absolute values", "percentages"],
    ["absolute values"],
    id="abs_val_dd",
    persistence=True,
    persistence_type="session",
)
user_dd = dcc.Dropdown(id="user_dd", multi=True, persistence=True, persistence_type="session")
mode_dd = dcc.Dropdown(id="mode_dd", multi=True, persistence=True, persistence_type="session")
move_dd = dcc.Dropdown(
    ["s", "d", "ds", "spl", "sur", "das", "h"],
    ["s", "d", "ds", "spl", "sur", "das", "h"],
    id="move_dd",
    multi=True,
    persistence=True,
    persistence_type="session",
)
layout = [
    dbc.Row(
        [
            dbc.Col(user_switch),
            dbc.Col(mode_switch),
            dbc.Col(move_switch),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(user_dd),
            dbc.Col(mode_dd),
            dbc.Col(move_dd),
        ]
    ),
    html.Div(id="stat_graphs"),
    dbc.Row(
        [
            dbc.Col(abs_val_dd, width=2),
        ]
    ),
]
