"""Serve the dash web app locally."""

from .app import app

if __name__ == "__main__":
    app.run(port=8050, debug=True)
