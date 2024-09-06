import unittest
import json
import sys
sys.path.append("..")
from main import app, get_db

class BookAPITest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS books')
            cursor.execute('''
                CREATE TABLE books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    publisher TEXT,
                    description TEXT,
                    UNIQUE (title, author, year)
                )
            ''')
            conn.commit()
            conn.close()

    def test_add_book(self):
        response = self.app.post('/books', json={
        "title": "Harry Potter and the Philosophers Stone",
        "author": "J.K. Rowling",
        "year": 1997,
        "publisher": "Bloomsbury (UK)",
        "description": "A book about a wizard boy"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)

    def test_add_duplicate_book(self):
        self.app.post('/books', json={
        "title": "Harry Potter and the Philosophers Stone",
        "author": "J.K. Rowling",
        "year": 1997,
        "publisher": "Bloomsbury (UK)",
        "description": "A book about a wizard boy"
        })
        response = self.app.post('/books', json={
        "title": "Harry Potter and the Philosophers Stone",
        "author": "J.K. Rowling",
        "year": 1997,
        "publisher": "Bloomsbury (UK)",
        "description": "A book about a wizard boy"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Book already exists', response.data.decode())

    def test_add_book_missing_fields(self):
        response = self.app.post('/books', json={
            'title': '',
            'author': 'Douglas Adams',
            'year': 1979
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid title', response.data.decode())

        response = self.app.post('/books', json={
            'title': 'The Great Gatsby',
            'author': '',
            'year': 1925
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid author', response.data.decode())

        response = self.app.post('/books', json={
            'title': 'The Hitchhikers Guide to the Galaxy',
            'author': 'Douglas Adams',
            'year': 'not a year'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid year', response.data.decode())

        response = self.app.post('/books', json={
            'title': 'The Hitchhikers Guide to the Galaxy',
            'author': 'Douglas Adams',
            'year': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid year', response.data.decode())

        response = self.app.post('/books', json={
            'title': 'The Hitchhikers Guide to the Galaxy',
            'author': 'Douglas Adams'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid year', response.data.decode())

    def test_get_all_books(self):
        self.app.post('/books', json={
            "id": 1,
            "title": "Harry Potter and the Philosophers Stone",
            "author": "J.K. Rowling",
            "year": 1997,
            "publisher": "Bloomsbury (UK)",
            "description": "A book about a wizard boy"
        })

        response = self.app.get('/books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['title'], 'Harry Potter and the Philosophers Stone')

    def test_get_book_by_id(self):
        response = self.app.post('/books', json=  {
            "id": 1,
            "title": "Harry Potter and the Philosophers Stone",
            "author": "J.K. Rowling",
            "year": 1997,
            "publisher": "Bloomsbury (UK)",
            "description": "A book about a wizard boy"
        })
        book_id = json.loads(response.data)['id']

        response = self.app.get(f'/books/{book_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Harry Potter and the Philosophers Stone')

    def test_filter_books(self):
        self.app.post('/books', json={
            "id": 1,
            "title": "Harry Potter and the Philosophers Stone",
            "author": "J.K. Rowling",
            "year": 1997,
            "publisher": "Bloomsbury (UK)",
            "description": "A book about a wizard boy"
        })
        self.app.post('/books', json={
            "id": 2,
            "title": "The Subtle Knife",
            "author": "Philip Pullman",
            "year": 1998,
            "publisher": "Scholastic Point",
            "description": ''
        })

        response = self.app.get('/books?author=J.K. Rowling')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['title'], 'Harry Potter and the Philosophers Stone')

        response = self.app.get('/books?year=1998')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['title'], 'The Subtle Knife')

    def test_delete_book(self):
        response = self.app.post('/books', json={
            "id": 1,
            "title": "Harry Potter and the Philosophers Stone",
            "author": "J.K. Rowling",
            "year": 1997,
            "publisher": "Bloomsbury (UK)",
            "description": "A book about a wizard boy"
        })
        book_id = json.loads(response.data)['id']

        response = self.app.delete(f'/books/{book_id}')
        self.assertEqual(response.status_code, 204)

        response = self.app.get(f'/books/{book_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)