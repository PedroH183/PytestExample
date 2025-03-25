import pytest
import library_management_system as library


@pytest.fixture
def sample_user():
    """ Dado que um usuário foi criado com seus atributos """

    return library.User(
        name="João Silva",
        email="joao_silva@teste.com.br",
        role = library.UserRole.MEMBER
    )

@pytest.fixture
def sample_borrow():
    """ Dado que um registro de empréstimo foi criado com seus atributos """

    return library.BorrowRecord(
        user_id="123",
        book_id="456"
    )

@pytest.fixture
def sample_book():
    """ Dado que um livro foi criado com seus atributos """
    return library.Book(
        title="O Senhor dos Anéis",
        author="J.R.R. Tolkien",
        isbn="978-3-16-148410-0",
        publication_year=1954,
        category="Fantasia"
    )


@pytest.fixture
def sample_libray_system():
    """ Dado que um sistema de biblioteca foi criado com seus atributos """

    return library.LibrarySystem()
