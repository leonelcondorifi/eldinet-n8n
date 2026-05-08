from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent / "eldinet.db"

SEED_CLIENTS = [
    {"id": 1, "name": "Ada Lovelace", "email": "ada.lovelace@example.com"},
    {"id": 2, "name": "Grace Hopper", "email": "grace.hopper@example.com"},
    {"id": 3, "name": "Alan Turing", "email": "alan.turing@example.com"},
]

SEED_USERS = [
    {"id": 1, "name": "Katherine Johnson", "email": "katherine.johnson@example.com"},
    {"id": 2, "name": "Margaret Hamilton", "email": "margaret.hamilton@example.com"},
    {"id": 3, "name": "Edsger Dijkstra", "email": "edsger.dijkstra@example.com"},
]


def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def _create_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )


def _seed_table(
    connection: sqlite3.Connection,
    table: str,
    rows: Iterable[dict[str, str | int]],
) -> None:
    count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if count:
        return
    connection.executemany(
        f"INSERT INTO {table} (id, name, email) VALUES (:id, :name, :email)",
        rows,
    )


def initialize_database(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with _connect(db_path) as connection:
        _create_tables(connection)
        _seed_table(connection, "clients", SEED_CLIENTS)
        _seed_table(connection, "users", SEED_USERS)
        connection.commit()


def fetch_clients() -> list[dict[str, str | int]]:
    initialize_database()
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, email FROM clients ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def fetch_users() -> list[dict[str, str | int]]:
    initialize_database()
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
