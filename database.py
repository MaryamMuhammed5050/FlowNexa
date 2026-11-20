import sqlite3
import hashlib
import secrets

DATABASE_NAME = "flownexa.db"


def get_connection():
    """Connect to the FlowNexa database."""
    return sqlite3.connect(DATABASE_NAME)

def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + ":" + password_hash.hex()
def initialize_database():
    """Create the database tables if they don't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

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

def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return "Username and password cannot be empty."

    password_hash = hash_password(password)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )

        return "Registration successful!"

    except sqlite3.IntegrityError:
        return "Username already exists."

def verify_password(password, stored_hash):
    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        original_hash = bytes.fromhex(hash_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        )

        return secrets.compare_digest(new_hash, original_hash)

    except (ValueError, TypeError, AttributeError):
        return False