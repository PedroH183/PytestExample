import pytest
import library_management_system as library


def test_sample_libray_system(sample_libray_system):
    """ Quando o sistema de biblioteca é criado, então os atributos devem ser inicializados corretamente """

    allowed_categories = ["Fiction", "Non-fiction", "Science", "History", "Biography", "Other"]

    assert sample_libray_system.books == {}
    assert sample_libray_system.users == {}
    assert sample_libray_system.borrow_records == {}

    assert allowed_categories == sample_libray_system.allowed_categories

def test_add_book(sample_libray_system):
    """ Quando um livro é adicionado, então ele deve ser adicionado ao sistema """

    sample_libray_system.add_book(
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1954,
        category="Fiction"
    )

    assert len(sample_libray_system.books) == 1


@pytest.mark.parametrize('title,author,isbn,publication_year,category', [
    ("", "J.K. Rowling", "978-3-16-148410-0", 1997, "Fiction"), # title invalid
    ("Harry Potter", "", "978-3-16-148410-0", 1997, "Fiction"), # author invalid
    ("Harry Potter", "J.K. Rowling", "", 1997, "Fiction"), # isbn invalid
    ("Harry Potter", "J.K. Rowling", "978-3-16-148410-0", 1997, ""), # category invalid
])
def test_add_book_with_wrong_category(title, author, isbn, publication_year, category, sample_libray_system):
    """ Um livro foi adicionado com atributos inválidos """

    true_condition = (
        "Title, author and ISBN are required",
        f"Category must be one of: {', '.join(sample_libray_system.allowed_categories)}",
        f"A book with ISBN {isbn} already exists"
    )
    try:
        sample_libray_system.add_book(
            isbn=isbn,
            title=title,
            author=author,
            category=category,
            publication_year=publication_year,
    )
    except ValueError as e:
        assert str(e) in true_condition
    finally:
        assert len(sample_libray_system.books) == 0


def test_get_book_by_id(sample_libray_system):
    """ Quando um livro é criado ele pode ser capturado pelo seu id """

    book_id = sample_libray_system.add_book(
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1954,
        category="Fiction"
    )
    assert book_id is not None
    book = sample_libray_system.get_book(book_id)

    assert book is not None

    book = book.to_dict()
    assert book['title'] == "O Senhor dos Anéis"
    assert book['author'] == "J.R.R. Tolkien"
    assert book['isbn'] == "978-3-16-148410-0"
    assert book['publication_year'] == 1954
    assert book['category'] == "Fiction"

def test_update_book(sample_libray_system):
    """ Quando um livro é atualizado, então ele deve ser atualizado no sistema """

    book_id = sample_libray_system.add_book(
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1954,
        category="Fiction"
    )

    assert book_id is not None

    result = sample_libray_system.update_book(book_id, **{
        "title": "O Hobbit",
        "author": "J.R.R. Tolkien"
    })
    assert result is True

    book = sample_libray_system.get_book(book_id)

    assert book is not None
    book = book.to_dict()
    assert book['title'] == "O Hobbit" # Alterado
    assert book['author'] == "J.R.R. Tolkien" # Alterado
    assert book['isbn'] == "978-3-16-148410-0"
    assert book['publication_year'] == 1954
    assert book['category'] == "Fiction"

def test_get_all_books(sample_libray_system):
    """ Quando todos os livros são capturados, então todos os livros devem ser retornados """

    sample_libray_system.add_book(
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1954,
        category="Fiction"
    )

    sample_libray_system.add_book(
        title="Harry Potter e a Pedra Filosofal",
        author="J.K. Rowling",
        isbn="978-3-16-148410-1",
        publication_year=1997,
        category="Fiction"
    )

    books = sample_libray_system.get_all_books(
        status=library.BookStatus.AVAILABLE
    )
    assert len(books) == 2

def test_query_book(sample_libray_system):
    """ Quando um livro é consultado, então ele deve ser retornado """

    sample_libray_system.add_book(
        title="Harry Potter e a Pedra Filosofal",
        author="J.K. Rowling",
        isbn="978-3-16-148410-1",
        publication_year=1997,
        category="Fiction"
    )
    sample_libray_system.add_book(
        title="O Senhor dos Anéis e a Pedra Filosofal",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1957,
        category="Fiction"
    )

    result = sample_libray_system.search_books("Harry Potter")

    assert isinstance(result, list)
    assert len(result) != 0 and len(result) == 1
    assert result[0].title == "Harry Potter e a Pedra Filosofal"

    result = sample_libray_system.search_books("Pedra Filosofal")

    assert isinstance(result, list)
    assert len(result) != 0 and len(result) == 2


# PARA USERS É QUASE A MESMA COISA ...

def test_borrow_book(sample_libray_system, sample_book, sample_user):
    """ Quando um livro é emprestado, então ele deve ser adicionado ao registro de empréstimos """

    sample_libray_system.books[sample_book.id] = sample_book
    sample_libray_system.users[sample_user.id] = sample_user

    borrow_id = sample_libray_system.borrow_book(
        sample_book.id, sample_user.id
    )
    assert borrow_id is not None
    assert isinstance(borrow_id, str)
    assert borrow_id in sample_user.borrowed_books
    assert sample_book.id in sample_libray_system.books
    assert sample_user.id in sample_libray_system.users
    assert sample_book.status == library.BookStatus.BORROWED



