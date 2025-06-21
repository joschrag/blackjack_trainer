"""Test app rendering."""

from dash.testing.application_runners import import_app


def test_render_app(dash_duo):
    app = import_app("blackjack_trainer.app")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#start_btn", "Deal Cards", timeout=4)
    assert dash_duo.find_element("#start_btn").text == "Deal Cards"
    for btn, text in zip(
        ["d", "sur", "h", "s", "spl"],
        [
            "double or hit (d)",
            "surrender (sur)",
            "hit (h)",
            "stand (s)",
            "split (spl)",
        ],
    ):
        assert dash_duo.find_element(f"#{btn}").text == text
