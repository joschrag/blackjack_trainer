"""This module initializes the database and contains the other submodules."""

import pathlib

import sqlalchemy as sa

db_file = pathlib.Path.cwd() / "db" / "db.sqlite"
if not db_file.exists():
    db_file.touch()
engine = sa.create_engine("sqlite:///db/db.sqlite")
