import sqlite3
import os


DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(__file__), "database.db"),
)


def connect_to_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_db_table():
    conn = connect_to_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_users():
    conn = connect_to_db()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_user_by_id(user_id):
    conn = connect_to_db()

    row = conn.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def insert_user(user):
    conn = connect_to_db()

    cursor = conn.execute(
        """
        INSERT INTO users (name, email, phone, address, country)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user["name"],
            user["email"],
            user["phone"],
            user["address"],
            user["country"]
        )
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return get_user_by_id(user_id)


def update_user(user):
    conn = connect_to_db()

    cursor = conn.execute(
        """
        UPDATE users
        SET name = ?, email = ?, phone = ?, address = ?, country = ?
        WHERE user_id = ?
        """,
        (
            user["name"],
            user["email"],
            user["phone"],
            user["address"],
            user["country"],
            user["user_id"]
        )
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return None

    return get_user_by_id(user["user_id"])


def patch_user(user_id, changes):
    existing_user = get_user_by_id(user_id)

    if existing_user is None:
        return None

    existing_user.update(changes)
    existing_user["user_id"] = user_id

    return update_user(existing_user)


def delete_user(user_id):
    conn = connect_to_db()

    cursor = conn.execute(
        "DELETE FROM users WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return cursor.rowcount > 0


if __name__ == "__main__":
    create_db_table()
    print("Database and users table created successfully.")
