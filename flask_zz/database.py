import sqlite3
import click
from flask import current_app, g


def open_database():
    if "database" not in g:
        g.database = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

        return g.database


def close_database(e=None):
    database = g.pop("database", None)

    if database is not None:
        database.close()

def init_database():
    database = open_database()

    with current_app.open_resource("schema.sql") as file:
        database.executescript(file.read().decode("utf-8"))

@click.command("init-database")
def init_database_command():
    init_database()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)
