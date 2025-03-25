import library_management_system as library


def test_book_creation(sample_book):
    """ Quando o livro é criado, então os atributos devem ser atribuídos corretamente """

    assert sample_book.title == "O Senhor dos Anéis"
    assert sample_book.author == "J.R.R. Tolkien"
    assert sample_book.isbn == "978-3-16-148410-0"
    assert sample_book.publication_year == 1954
    assert sample_book.category == "Fantasia"
    assert sample_book.status == library.BookStatus.AVAILABLE

def test_update_status(sample_book):
    """ Quando o livro é atualizado, então os atributos devem ser atualizados corretamente """

    before_update_timestamp = sample_book.last_updated

    sample_book.update_status(library.BookStatus.LOST)

    assert sample_book.status != library.BookStatus.AVAILABLE
    assert sample_book.last_updated != before_update_timestamp

def test_to_dict_book(sample_book):
    """ Quando o livro é convertido para dicionário, então os atributos devem ser convertidos corretamente """

    book_dict = sample_book.to_dict()

    assert book_dict["title"] == "O Senhor dos Anéis"
    assert book_dict["author"] == "J.R.R. Tolkien"
    assert book_dict["isbn"] == "978-3-16-148410-0"
    assert book_dict["publication_year"] == 1954
    assert book_dict["category"] == "Fantasia"
    assert book_dict["status"] == library.BookStatus.AVAILABLE.value

    assert "added_date" in book_dict
    assert "last_updated" in book_dict
