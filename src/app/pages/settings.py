"""This script defines the page layout for the /settings page."""

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

dash.register_page(
    __name__,
    path="/settings",
    name="Blackjack Trainer Settings",
    title="Blackjack Trainer Settings",
    description="Settings page.",
)
das_label = html.Label("Is doubling allowed after splitting?")

das_dd_train = dcc.Dropdown(["das", "Allowed", "Forbidden"])
das_dd = dcc.Dropdown(["Allowed", "Forbidden"])
soft_17_label = "Dealer hits on soft 17"
soft_17_sw = dmc.Switch(onLabel="Hit", offLabel="Stand", size="xl")
double_label = "When is doubling allowed?"
double_dd = dcc.Dropdown(["any first tow cards", "9-11 only", "10-11 only"])
num_split_label = html.Label("How many hands can a player split to ?")
split_dd = dcc.Dropdown(
    [{"label": "2 hands", "value": 2}, {"label": "3 hands", "value": 3}, {"label": "4 hands", "value": 4}]
)
split_label = html.Label("Can split Aces more than once")
split_sw = dmc.Switch(offLabel="no", onLabel="yes", size="xl")
shoe_label = html.Label("How many decks are played before shuffling?")
shoesize_input = dcc.Input(1, type="number", min=1, max=10)
shoesize_input_train = dcc.Input(1, type="number", min=1, max=10)


layout: list = [
    html.Div(
        dmc.Accordion(
            value=["general"],
            multiple=True,
            children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "General Settings", icon=DashIconify(icon="material-symbols:settings", width=30)
                        ),
                        dmc.AccordionPanel(["TBD"]),
                    ],
                    value="general",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "Game Settings", icon=DashIconify(icon="material-symbols:playing-cards-outline", width=30)
                        ),
                        dmc.AccordionPanel(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(shoe_label, width=4),
                                        dbc.Col(das_label, width=4),
                                        dbc.Col(num_split_label, width=4),
                                    ],
                                    className="settingrow",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(shoesize_input, width=4),
                                        dbc.Col(das_dd, width=4),
                                        dbc.Col(split_dd, width=4),
                                    ],
                                    className="settingrow",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(soft_17_label, width=4),
                                        dbc.Col(split_label, width=4),
                                        dbc.Col(double_label, width=4),
                                    ],
                                    className="settingrow",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(soft_17_sw, width=4),
                                        dbc.Col(split_sw, width=4),
                                        dbc.Col(double_dd, width=4),
                                    ],
                                    className="settingrow",
                                ),
                            ]
                        ),
                    ],
                    value="game",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "Training Settings", icon=DashIconify(icon="material-symbols:playing-cards", width=30)
                        ),
                        dmc.AccordionPanel(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(shoe_label, width=4),
                                        dbc.Col(das_label, width=4),
                                    ],
                                    className="settingrow",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(shoesize_input_train, width=4),
                                        dbc.Col(das_dd_train, width=4),
                                    ],
                                    className="settingrow",
                                ),
                            ]
                        ),
                    ],
                    value="training",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "Bot Settings", icon=DashIconify(icon="material-symbols:engineering-sharp", width=30)
                        ),
                        dmc.AccordionPanel("TBD"),
                    ],
                    value="bot",
                ),
            ],
        ),
        id="settings",
    ),
]
