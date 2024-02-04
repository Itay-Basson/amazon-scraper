import sqlite3
from sqlite3 import Error


DATABASE_NAME = "search_history.db"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Error as e:
        print(e)

    return conn


def create_table():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS search_history (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              asin TEXT NOT NULL,                              
                              amazon_us REAL,
                              amazon_uk REAL,
                              amazon_de REAL,
                              amazon_ca REAL,
                              time TEXT NOT NULL)
                           ''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()


def insert_search_history(search_history):
    connection = create_connection()
    cursor = connection.cursor()

    # Insert the search history record into the search_history table
    cursor.execute(
        """
        INSERT INTO search_history (name, asin, amazon_us, amazon_uk, amazon_de, amazon_ca, time)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (
            search_history['name'],
            search_history['asin'],
            search_history['amazon_us'],
            search_history['amazon_uk'],
            search_history['amazon_de'],
            search_history['amazon_ca'],
            search_history['time'],
        )
    )

    connection.commit()
    connection.close()


def get_past_searches():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM search_history")
    rows = cursor.fetchall()

    search_history = [
        {
            "name": row[1],
            "asin": row[2],
            "amazon_us": row[3],
            "amazon_uk": row[4],
            "amazon_de": row[5],
            "amazon_ca": row[6],
            "time": row[7],
        }
        for row in rows
    ]

    connection.close()
    return search_history



create_table()
