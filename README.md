Book Collection API <br />

This project implements a web backend for managing a collection of books. <br />
The API supports adding, retrieving, filtering, and deleting books from a SQLite database. <br />
It is built using Python, Flask, and SQLite, and is designed to run locally on port 9000. Unit tests are provided for testing the API functionality. <br />


Project structure: <br />
. <br />
├── /tests <br />
|    └unit_tests.py           # Unit tests for the API <br />
├── db_setup.py               # Script to create the SQLite database and table <br />
├── main.py                   # Main application file <br />
├── requests.txt              # Example API requests for testing <br />
├── requirements.txt          # List of dependencies <br />
└── README.md <br />

Requirements and dependencies: <br />
Python 3.x <br />
Flask <br />
SQLite3 <br />

The necessary dependencies can be installed using: pip install Flask <br />

Getting Started: <br />
    1. Clone the repository.  <br />

    2. Run db_setup.py to create the database using the command: python db_setup.py
        This will create the database and add books.db to the project folder.

    3. Start the Flask server using the command: python main.py
        You will get a prompt in your terminal and the API will run locally on http://localhost:9000

    4. Now you can interact with the API using tools such as Postman or curl. The file requests.txt contains requests that can be used to test the API.

API Endpoints: <br />

Add a book: <br />
POST /books <br />

Request body: <br />
{ <br />
  "title": "Book Title", <br />
  "author": "Author Name", <br />
  "year": 2024, <br />
  "publisher": "Publisher Name", <br />
  "description": "Description" <br />
}

Retrieve books: <br />
GET /books <br />

Optional query parameters: author, year & publisher <br />

Retrieve a specific book: <br />
GET /books/id <br />

Delete  a book: <br />
DELETE /books/id <br />

Unit tests: <br />
You can find the unit tests in the folder tests in file unit_tests.py and you can run the tests using command: python unit_tests.py <br />
Unit tests create a separate books.db in the tests folder. <br />
