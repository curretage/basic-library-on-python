import sqlite3
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)

DATABASE_NAME = 'lib.db'  # sql db file name

def initialize_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)  # conn to the sqlite database
        cursor = conn.cursor()

        # create 'books' table if it doesn't exist, defining the structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                status TEXT
            )
        ''')
        conn.commit()  # commit changes to the database
        print(f"Database '{DATABASE_NAME}' initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()  # ensure the connection is closed

def add_book(title, author, year, genre, status):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)  # connect to the database
        cursor = conn.cursor()

        # insert a new book, using placeholders for SQL injection prevention
        cursor.execute('''
            INSERT INTO books (title, author, year, genre, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, year, genre, status))

        conn.commit()  # commit the transaction
        return True  # indicate success
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")
        return False
    finally:
        if conn:
            conn.close()

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Input fields for book details
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Title")
        self.layout.addWidget(self.title_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Author")
        self.layout.addWidget(self.author_input)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText("Year")
        self.layout.addWidget(self.year_input)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText("Genre")
        self.layout.addWidget(self.genre_input)

        self.status_input = QLineEdit(self)
        self.status_input.setPlaceholderText("Status (e.g. read, unread)")
        self.layout.addWidget(self.status_input)

        # button to add the book to the db
        self.add_button = QPushButton("Add Book", self)
        self.add_button.clicked.connect(self.add_book_to_db)  # connect button action
        self.layout.addWidget(self.add_button)

        self.status_label = QLabel("", self)  # label to show messages
        self.layout.addWidget(self.status_label)

    def add_book_to_db(self):
        # gather data from input fields
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        genre = self.genre_input.text()
        status = self.status_input.text()

        if add_book(title, author, year, genre, status):
            QMessageBox.information(self, "Success", f"Book '{title}' added successfully.")
            self.clear_inputs()  # clear input fields
        else:
            QMessageBox.critical(self, "Error", "Failed to add book.")

    def clear_inputs(self):
        # clear all input fields
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.genre_input.clear()
        self.status_input.clear()

if __name__ == "__main__":
    initialize_database()  # initialize the database

    app = QApplication(sys.argv)  # create the application instance
    window = LibraryApp()  # create the main window
    window.show()  # show the window
    sys.exit(app.exec())  # start the application event loop