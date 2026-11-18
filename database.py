
import sqlite3

DATABASE_NAME = "flownexa.db"


def get_connection():
    """Connect to the FlowNexa database."""
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """Create the messages table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_message(role, content):
    """Save a conversation message."""

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO messages (role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )


def get_history(limit=12):
    """Retrieve the most recent conversation messages."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        messages = cursor.fetchall()

    return [
        {"role": role, "content": content}
        for role, content in reversed(messages)
    ]


def clear_history():
    """Clear conversation history."""

    with get_connection() as connection:
        connection.execute("DELETE FROM messages")


initialize_database()
