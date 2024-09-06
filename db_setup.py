import sqlite3

def create_db():
    try:
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                publisher TEXT,
                description TEXT,
                UNIQUE(title, author, year)
            )
        ''')
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_db()