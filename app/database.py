import sqlite3

import click
from flask import current_app, g


def get_db():
    """Return the SQLite connection for the current application context."""
    if "db" not in g:
        db = sqlite3.connect(current_app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        g.db = db
    return g.db


def close_db(exception=None):
    """Close the database connection at the end of the application context."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the database schema if it does not exist yet."""
    db = get_db()
    with current_app.open_resource("schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf-8"))
    db.commit()


@click.command("init-db")
def init_db_command():
    """Initialize the database schema."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database helpers and CLI commands with the application."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
