Book Collection API

This project implements a web backend for managing a collection of books.
The API supports adding, retrieving, filtering, and deleting books from a SQLite database.
It is built using Python, Flask, and SQLite, and is designed to run locally on port 9000. Unit tests are provided for testing the API functionality.


Project structure:
.
├── /tests
|    └unit_tests.py           # Unit tests for the API
├── db_setup.py               # Script to create the SQLite database and table
├── main.py                   # Main application file
├── requests.txt              # Example API requests for testing
├── requirements.txt          # List of dependencies
└── README.md

Requirements and dependencies:
Python 3.x
Flask
SQLite3

The necessary dependencies can be installed using: pip install Flask

Getting Started:
    1. Clone the repository.

    2. Run db_setup.py to create the database using the command: python db_setup.py
        This will create the database and add books.db to the project folder.

    3. Start the Flask server using the command: python main.py
        You will get a prompt in your terminal and the API will run locally on http://localhost:9000

    4. Now you can interact with the API using tools such as Postman or curl. The file requests.txt contains requests that can be used to test the API.

API Endpoints:

Add a book:
POST /books

Request body:
{
  "title": "Book Title",
  "author": "Author Name",
  "year": 2024,
  "publisher": "Publisher Name",
  "description": "Description"
}

Retrieve books:
GET /books

Optional query parameters: author, year & publisher

Retrieve a specific book:
GET /books/id

Delete  a book:
DELETE /books/id

Unit tests: 
You can find the unit tests in the folder tests in file unit_tests.py and you can run the tests using command: python unit_tests.py
Unit tests create a separate books.db in the tests folder.