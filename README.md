# Library Management System

A comprehensive Python-based library management system for tracking books, users, and lending operations.
To Study about tests

## Features

- 📚 Book Management
  - Add, update and track books
  - Search by title, author, or ISBN
  - Categorize books
  - Monitor book status (available, borrowed, maintenance, lost)

- 👥 User Management
  - Multiple users roles (admin, librarian, member)
  - Track borrowed books per user
  - User activation/deactivation
  - Borrowing limit

- 📖 Borrowing System
  - Book checkout and return
  - Due date management
  - Extension handling
  - Overdue track

## Usage

```python
from library_management_system import LibrarySystem

# Initializee the system
library = LibrarySystem()

# Add a book
book_id = library.add_book(
    title="The Lord of the Rings",
    author="J.R.R. Tolkien",
    isbn="978-3-16-148410-0",
    publication_year=1954,
    category="Fiction"
)

# Add a user
user_id = library.add_user(
    name="John Doe",
    email="john@example.com"
)

# Borrow a book
borrow_id = library.borrow_book(book_id, user_id)
```

## Testing

The project incldes test coverage using pytest:

```bash
# Run all tests
pytest
```

## Project Structure

```
LearningTestes/
├── library_management_system.py   # Core implementation
├── test_book_flow.py             # Book tests
├── test_borrow_record.py         # Borrowing tests
├── test_library_system_flow.py   # System tests
├── test_user_flow.py            # User tests
├── conftest.py                  # Test fixtures
└── requirements.txt             # Dependencies
```
