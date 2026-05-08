from __future__ import annotations

import os
import sqlite3
import threading
from pathlib import Path

_DEFAULT_DB_PATH = Path(__file__).resolve().parent / "app.db"
DB_PATH = Path(os.getenv("ELDINET_DB_PATH", str(_DEFAULT_DB_PATH))).expanduser().resolve()
_INITIALIZE_LOCK = threading.Lock()
_INITIALIZED_PATHS: set[Path] = set()

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


def _seed_clients(connection: sqlite3.Connection) -> None:
    connection.executemany(
        "INSERT OR IGNORE INTO clients (id, name, email) VALUES (:id, :name, :email)",
        SEED_CLIENTS,
    )


def _seed_users(connection: sqlite3.Connection) -> None:
    connection.executemany(
        "INSERT OR IGNORE INTO users (id, name, email) VALUES (:id, :name, :email)",
        SEED_USERS,
    )


def _initialize_database(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with _connect(db_path) as connection:
        _create_tables(connection)
        _seed_clients(connection)
        _seed_users(connection)
        connection.commit()


def initialize_database(db_path: Path = DB_PATH) -> None:
    db_path = db_path.expanduser().resolve()
    with _INITIALIZE_LOCK:
        if db_path in _INITIALIZED_PATHS:
            return
        _initialize_database(db_path)
        _INITIALIZED_PATHS.add(db_path)


def _ensure_initialized() -> None:
    initialize_database(DB_PATH)


def fetch_clients() -> list[dict[str, str | int]]:
    _ensure_initialized()
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, email FROM clients ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def fetch_users() -> list[dict[str, str | int]]:
    _ensure_initialized()
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
