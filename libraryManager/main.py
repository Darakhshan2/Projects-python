import sqlite3
import streamlit as st

connection = sqlite3.connect("books_data.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    genre TEXT,
    read INTEGER 
)
""")
connection.commit()

class BookCollection:
    """A class to manage a collection of books using an SQLite database."""

    def __init__(self):
        """Initialize the book collection and set up the SQLite database."""
        self.connection = sqlite3.connect("books_data.db") 
        self.cursor = self.connection.cursor() 
        self._create_table()  

    def _create_table(self):
        """Create the 'books' table if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                genre TEXT,
                read INTEGER
            )
        """)
        self.connection.commit() 
    def create_new_book(self, book_title, book_author, publication_year, book_genre, is_book_read):
        """Add a new book to the database."""
        self.cursor.execute("""
            INSERT INTO books (title, author, publication_year, genre, read)
            VALUES (?, ?, ?, ?, ?)
        """, (book_title, book_author, publication_year, book_genre, is_book_read))
        self.connection.commit()  

    def delete_book(self, book_title):
        """Remove a book from the database using its title."""
        self.cursor.execute("DELETE FROM books WHERE title = ?", (book_title,))
        if self.cursor.rowcount > 0:  
            self.connection.commit()  
            return True
        else:
            return False

    def find_book(self, search_type, search_text):
        """Search for books in the database by title or author name."""
        if search_type == "Title":
            self.cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ?", (f"%{search_text.lower()}%",))
        elif search_type == "Author":
            self.cursor.execute("SELECT * FROM books WHERE LOWER(author) LIKE ?", (f"%{search_text.lower()}%",))
        return self.cursor.fetchall()  

    def update_book(self, book_title, new_title, new_author, new_year, new_genre, new_read):
        """Modify the details of an existing book in the database."""
        self.cursor.execute("SELECT * FROM books WHERE title = ?", (book_title,))
        book = self.cursor.fetchone()
        if book:
            self.cursor.execute("""
                UPDATE books
                SET title = ?, author = ?, publication_year = ?, genre = ?, read = ?
                WHERE id = ?
            """, (new_title, new_author, new_year, new_genre, new_read, book[0]))
            self.connection.commit() 
            return True
        else:
            return False

    def show_all_books(self):
        """Display all books in the database with their details."""
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()[0] 
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE read = 1")
        completed_books = self.cursor.fetchone()[0]  
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        return total_books, completion_rate

def main(book_manager):
    st.title("Personal Library Manager 📚")

    st.sidebar.title("Menu")
    action = st.sidebar.radio("Actions :", ["Add a new book", "Remove a book", "Search for books", "Update book details", "View all books", "View reading progress"])

    st.write("Welcome to your personal library manager!")

    if action == "Add a new book":
        st.subheader("Add a new book 📕")
        book_title = st.text_input("Enter the title of the book:")
        book_author = st.text_input("Enter the author of the book:")
        publication_year = st.number_input("Enter the publication year of the book:", min_value=0)
        book_genre = st.text_input("Enter the genre of the book:")
        is_book_read = st.radio("Have you read the book?", ["Yes", "No"]) == "Yes"

        if st.button("Add Book"):
            book_manager.create_new_book(book_title, book_author, publication_year, book_genre, is_book_read)
            st.success("Book added successfully!")

    elif action == "Remove a book":
        st.subheader("Remove a book ❌")
        book_title = st.text_input("Enter the title of the book you want to remove:")

        if st.button("Remove Book"):
            if book_manager.delete_book(book_title):
                st.success("Book deleted successfully!")
            else:
                st.error("Book not found!")

    elif action == "Search for books":
        st.subheader("Search for books 🔍")
        search_type = st.radio("Search by:", ["Title", "Author"])
        search_text = st.text_input("Enter the search text:")
        if st.button("Search"):
            found_books = book_manager.find_book(search_type, search_text)
            if found_books:
                st.write("Found books:")
                for index, book in enumerate(found_books, 1):
                    st.write(f"{index}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
            else:
                st.info("No books found!")

    elif action == "Update book details":
        st.subheader("Update book details 📃")
        book_title = st.text_input("Enter the title of the book you want to edit:")
        if st.button("Find Book"):
            book_manager.cursor.execute("SELECT * FROM books WHERE title = ?", (book_title,))
            book = book_manager.cursor.fetchone()
            if book:
                new_title = st.text_input("New title:", book[1])
                new_author = st.text_input("New author:", book[2])
                new_year = st.number_input("New year:", book[3])
                new_genre = st.text_input("New genre:", book[4])
                new_read = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"
                if st.button("Update Book"):
                    if book_manager.update_book(book_title, new_title, new_author, new_year, new_genre, new_read):
                        st.success("Book updated successfully!")
                    else:
                        st.error("Book not found!")
            else:
                st.error("Book not found!")

    elif action == "View all books":
        st.subheader("View all books 📔")
        books = book_manager.show_all_books()
        if books:
            st.write("Your Book Collection:")
            for index, book in enumerate(books, 1):
                st.write(f"{index}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
        else:
            st.info("Your collection is empty!")

    elif action == "View reading progress":
        st.subheader("View reading progress 📖")
        total_books, completion_rate = book_manager.show_reading_progress()
        st.write(f"Total books in collection: {total_books}")
        st.write(f"Reading progress: {completion_rate:.2f}%")

if __name__ == "__main__":
    book_manager = BookCollection()
    main(book_manager)