from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'books.db'

def get_db():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    
    except sqlite3.DatabaseError as e:
        print(f"Error connecting to database: {e}")
        abort(500, description="Database connection failed")

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json

    if not data.get('title'):
        return abort(400, description="Invalid title")
    
    elif not data.get('author'):
        return abort(400, description="Invalid author")
    
    elif not isinstance(data.get('year'), int):
        return abort(400, description="Invalid year")

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR IGNORE INTO books (title, author, year, publisher, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['title'], data['author'], data['year'], data.get('publisher'), data.get('description')))

        if cursor.rowcount == 0:
            return abort(400, description="Book already exists")

        conn.commit()
        book_id = cursor.lastrowid

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return abort(500, description="Database error")

    finally:
        conn.close()

    return jsonify({"id": book_id}), 200

@app.route('/books', methods=['GET'])
def get_books():
    author = request.args.get('author')
    year = request.args.get('year')
    publisher = request.args.get('publisher')

    try:
        conn = get_db()
        cursor = conn.cursor()

        query = 'SELECT * FROM books WHERE 1=1'
        params = []

        if author:
            query += ' AND author = ?'
            params.append(author)
        if year:
            if not year.isdigit():
                return abort(400, description="Invalid year")
            query += ' AND year = ?'
            params.append(int(year))
        if publisher:
            query += ' AND publisher = ?'
            params.append(publisher)

        cursor.execute(query, params)
        books = cursor.fetchall()

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return abort(500, description="Database query error")
    
    finally: 
        conn.close()

    return jsonify([{
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "year": book[3],
        "publisher": book[4],
        "description": book[5]
    } for book in books]), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return abort(500, description="Database query error")
    
    finally:
        conn.close()

    if not book:
        return abort(404, description="Book not found")

    return jsonify({
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "year": book[3],
        "publisher": book[4],
        "description": book[5]
    }), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError: {e}")
        return abort(500, description="Database error during deletion")
    
    finally:
        conn.close()

    if cursor.rowcount == 0:
        return abort(404, description="Book not found")

    return '', 204

if __name__ == '__main__':
    app.run(port=9000)