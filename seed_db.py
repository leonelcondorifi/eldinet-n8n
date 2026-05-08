from app.db import DB_PATH, initialize_database


def main() -> None:
    initialize_database()
    print(f"SQLite database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
