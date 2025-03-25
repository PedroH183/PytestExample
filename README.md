# Library Management System

This is a Python-based library management system to keep track of books, users, and lending operations. The focus here is write tests for this project ! 

## Features

### Book Management
- Add, update, and keep tabs on books
- Search by title, author, or ISBN
- Categorize books however you like
- See if a book is available, borrowed, under maintenance, or lost

### User Management
- Different user roles: admin, librarian, and member
- Track which books each user has borrowed
- Set borrowing limits to keep things under control

### Borrowing System
- Handle checkouts and returns easily
- Keep track of due dates
- Detect overdue books

## Running Tests

Just run:

```bash
pytest
```

## Project Structure

```
LearningTestes/
├── library_management_system.py  # Core logic of the system
├── test_book_flow.py             # Tests for book-related functions
├── test_borrow_record.py         # Tests for borrowing records
├── test_library_system_flow.py   # Full system tests
├── test_user_flow.py             # Tests for user management
├── conftest.py                   # Test fixtures and setup
└── requirements.txt              # List of dependencies
```

## Next Steps ...

Write tests with **mocked data**, using `unittest.mock.MagicMock` to simulate database interactions and other dependencies.

### Mocking Example

```python
from unittest.mock import MagicMock
from library_management_system import LibrarySystem

def test_mocked_borrow():
    # Create a mock instance of LibrarySystem
    # Arrange
    library = MagicMock()

    library.add_book.return_value = 1
    library.add_user.return_value = 10
    library.borrow_book.return_value = 100

    # Act
    book_id = library.add_book( "Mocked Book", "Mocked Author", "1234567890", 2022, "Fiction" )
    user_id = library.add_user( "Test User", "test@example.com" )
    borrow_id = library.borrow_book( book_id, user_id )

    # Assert
    assert borrow_id == 100
```
To improve in test you can search about [Triple A](https://medium.com/@pablodarde/o-padr%C3%A3o-triple-a-arrange-act-assert-741e2a94cf88) and [pytest-ddd](https://github.com/pgorecki/python-ddd/tree/main)
