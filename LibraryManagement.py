import mysql.connector

class Library:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9141639744",
            database="library_db"
        )
        self.cursor = self.conn.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                available BOOLEAN NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def add_book(self, title, author):
        insert_query = "INSERT INTO books (title, author, available) VALUES (%s, %s, %s)"
        book_data = (title, author, True)
        self.cursor.execute(insert_query, book_data)
        self.conn.commit()

    def list_books(self):
        self.cursor.execute("SELECT id, title, author, available FROM books")
        books = self.cursor.fetchall()
        for idx, book in enumerate(books, start=1):
            availability = "Available" if book[3] else "Not Available"
            print(f"{idx}. Title: {book[1]}, Author: {book[2]}, Status: {availability}")

    def borrow_book(self, title):
        update_query = "UPDATE books SET available = %s WHERE title = %s AND available = %s"
        self.cursor.execute(update_query, (False, title, True))
        if self.cursor.rowcount > 0:
            print(f"Successfully borrowed '{title}'.")
            self.conn.commit()
        else:
            print(f"'{title}' is not available for borrowing.")

    def return_book(self, title):
        update_query = "UPDATE books SET available = %s WHERE title = %s AND available = %s"
        self.cursor.execute(update_query, (True, title, False))
        if self.cursor.rowcount > 0:
            print(f"Successfully returned '{title}'.")
            self.conn.commit()
        else:
            print(f"'{title}' is not a valid book to return or is already available.")

def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add a book")
        print("2. List all books")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)
            print(f"'{title}' by {author} has been added to the library.")

        elif choice == "2":
            library.list_books()

        elif choice == "3":
            title = input("Enter the title of the book you want to borrow: ")
            library.borrow_book(title)

        elif choice == "4":
            title = input("Enter the title of the book you want to return: ")
            library.return_book(title)

        elif choice == "5":
            print("Exiting the program.")
            library.conn.close()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
