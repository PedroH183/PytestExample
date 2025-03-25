import uuid
from enum import Enum
from datetime import datetime, timedelta


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    MAINTENANCE = "maintenance"
    LOST = "lost"


class UserRole(Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    MEMBER = "member"


class Book:
    def __init__(self, title, author, isbn, publication_year, category):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.category = category
        self.status = BookStatus.AVAILABLE
        self.added_date = datetime.now()
        self.last_updated = datetime.now()

    def update_status(self, new_status):
        if not isinstance(new_status, BookStatus):
            raise TypeError("Status must be a BookStatus enum")
        self.status = new_status
        self.last_updated = datetime.now()
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "category": self.category,
            "status": self.status.value,
            "added_date": self.added_date.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }


class User:
    def __init__(self, name, email, role=UserRole.MEMBER):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role
        self.joined_date = datetime.now()
        self.active = True
        self.borrowed_books = []  # List of BorrowRecord IDs

    def can_borrow(self, max_books=3):
        return len(self.borrowed_books) <= max_books and self.active

    def deactivate(self):
        self.active = False
        return True

    def reactivate(self):
        self.active = True
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "joined_date": self.joined_date.isoformat(),
            "active": self.active,
            "borrowed_books": self.borrowed_books
        }


class BorrowRecord:
    def __init__(self, book_id, user_id, borrow_days=14):
        self.id = str(uuid.uuid4())
        self.book_id = book_id
        self.user_id = user_id

        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=borrow_days)
        self.return_date = None
        self.is_returned = False
        self.extended = False

    def return_book(self):
        if self.is_returned:
            return False
        self.return_date = datetime.now()
        self.is_returned = True
        return True

    def extend_borrow(self, additional_days=7):
        """ Não é possivel extender o emprestimo se o livro já foi devolvido ou se o prazo já passou """

        if self.extended or self.is_returned or datetime.now() > self.due_date:
            return False
        self.due_date += timedelta(days=additional_days)
        self.extended = True
        return True

    def is_overdue(self):
        return not self.is_returned and datetime.now() > self.due_date

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "borrow_date": self.borrow_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "is_returned": self.is_returned,
            "extended": self.extended,
            "is_overdue": self.is_overdue()
        }


class LibrarySystem:
    def __init__(self):
        self.books = {}  # book_id -> Book
        self.users = {}  # user_id -> User
        self.borrow_records = {}  # record_id -> BorrowRecord
        self.allowed_categories = ["Fiction", "Non-fiction", "Science", "History", "Biography", "Other"]

    def add_book(self, title, author, isbn, publication_year, category):
        if not title or not author or not isbn:
            raise ValueError("Title, author and ISBN are required")

        if category not in self.allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(self.allowed_categories)}")

        # Check for duplicate ISBN
        for book in self.books.values():
            if book.isbn == isbn:
                raise ValueError(f"A book with ISBN {isbn} already exists")

        book = Book(title, author, isbn, publication_year, category)
        self.books[book.id] = book
        return book.id

    def update_book(self, book_id, **kwargs):
        if book_id not in self.books:
            raise ValueError("Book not found")

        book = self.books[book_id]
        valid_fields = ["title", "author", "publication_year", "category"]

        for field, value in kwargs.items():
            if field in valid_fields:
                setattr(book, field, value)
                book.last_updated = datetime.now()

        return True

    def get_book(self, book_id):
        if book_id not in self.books:
            return None
        return self.books[book_id]

    def get_all_books(self, status=None, category=None):
        result = list(self.books.values())

        if status:
            result = [book for book in result if book.status == status]

        if category:
            result = [book for book in result if book.category == category]

        return result

    def search_books(self, query):

        query = query.lower()
        results = []

        for book in self.books.values():
            if (query in book.title.lower() or
                query in book.author.lower() or
                query in book.isbn.lower() or
                query == book.publication_year):
                results.append(book)

        return results

    def add_user(self, name, email, role=UserRole.MEMBER):
        if not name or not email:
            raise ValueError("Name and email are required")

        # Check for duplicate email
        for user in self.users.values():
            if user.email == email:
                raise ValueError(f"A user with email {email} already exists")

        user = User(name, email, role)
        self.users[user.id] = user
        return user.id

    def get_user(self, user_id):
        if user_id not in self.users:
            return None
        return self.users[user_id]

    def get_all_users(self, role=None, active_only=True):
        result = list(self.users.values())

        if role:
            result = [user for user in result if user.role == role]

        if active_only:
            result = [user for user in result if user.active]

        return result

    def borrow_book(self, book_id, user_id, borrow_days=14):
        if book_id not in self.books:
            raise ValueError("Book not found")

        if user_id not in self.users:
            raise ValueError("User not found")

        book = self.books[book_id]
        user = self.users[user_id]

        if book.status != BookStatus.AVAILABLE:
            raise ValueError(f"Book is not available, current status: {book.status.value}")

        if not user.can_borrow():
            raise ValueError("User cannot borrow more books")

        borrow_record = BorrowRecord(book_id, user_id, borrow_days)
        self.borrow_records[borrow_record.id] = borrow_record

        # Update book status
        book.update_status(BookStatus.BORROWED)

        # Update user's borrowed books
        user.borrowed_books.append(borrow_record.id)

        return borrow_record.id

    def return_book(self, record_id):
        if record_id not in self.borrow_records:
            raise ValueError("Borrow record not found")

        record = self.borrow_records[record_id]

        if record.is_returned:
            raise ValueError("Book already returned")

        # Update record
        record.return_book()

        # Update book status
        book = self.books[record.book_id]
        book.update_status(BookStatus.AVAILABLE)

        # Update user's borrowed books
        user = self.users[record.user_id]
        user.borrowed_books.remove(record_id)

        return True

    def extend_borrowing(self, record_id, additional_days=7):
        if record_id not in self.borrow_records:
            raise ValueError("Borrow record not found")

        record = self.borrow_records[record_id]

        if not record.extend_borrow(additional_days):
            raise ValueError("Cannot extend this borrowing")

        return True

    def get_overdue_books(self):
        overdue_records = []

        for record in self.borrow_records.values():
            if record.is_overdue():
                overdue_records.append({
                    "record": record,
                    "book": self.books[record.book_id],
                    "user": self.users[record.user_id]
                })

        return overdue_records

    def get_borrow_history(self, user_id=None, book_id=None):
        results = list(self.borrow_records.values())

        if user_id:
            results = [record for record in results if record.user_id == user_id]

        if book_id:
            results = [record for record in results if record.book_id == book_id]

        return results

    def generate_reports(self):
        total_books = len(self.books)
        available_books = len([b for b in self.books.values() if b.status == BookStatus.AVAILABLE])
        borrowed_books = len([b for b in self.books.values() if b.status == BookStatus.BORROWED])

        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.active])

        books_by_category = {}
        for book in self.books.values():
            if book.category not in books_by_category:
                books_by_category[book.category] = 0
            books_by_category[book.category] += 1

        current_borrows = len([r for r in self.borrow_records.values() if not r.is_returned])
        overdue_borrows = len([r for r in self.borrow_records.values() if r.is_overdue()])

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_users": total_users,
            "active_users": active_users,
            "books_by_category": books_by_category,
            "current_borrows": current_borrows,
            "overdue_borrows": overdue_borrows
        }
