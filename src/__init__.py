import pathlib

import sqlalchemy as sa

db_file = pathlib.Path.cwd() / "db" / "db.sqlite"
if not db_file.exists():
    with open(db_file, "w") as fp:
        pass
engine = sa.create_engine("sqlite:///db/db.sqlite")
