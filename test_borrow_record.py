from datetime import datetime


def test_borrow_record_to_dict(sample_borrow):
    """ Quando o registro de empréstimo é convertido em dicionário, então os atributos devem ser convertidos corretamente """

    borrow_dict = sample_borrow.to_dict()
    assert 'id' in borrow_dict
    assert borrow_dict['user_id'] == "123"
    assert borrow_dict['book_id'] == "456"
    assert borrow_dict['return_date'] is None
    assert borrow_dict['due_date'] is not None
    assert borrow_dict['borrow_date'] is not None
    assert borrow_dict['is_returned'] == False
    assert borrow_dict['extended'] == False


def test_borrow_record_return(sample_borrow):
    """ Quando o registro de empréstimo é retornado, então o status deve ser atualizado corretamente """

    result = sample_borrow.return_book()

    assert result is True

    result = sample_borrow.return_book()

    assert result is False
    assert sample_borrow.is_returned == True
    assert sample_borrow.return_date is not None

def test_borrow_record_extend(sample_borrow):
    """ Quando o registro de empréstimo é estendido, então o status deve ser atualizado corretamente """

    assert sample_borrow.extended == False
    assert sample_borrow.is_returned == False
    assert datetime.now() < sample_borrow.due_date

    result = sample_borrow.extend_borrow()

    assert result is True

    result = sample_borrow.extend_borrow()

    assert result is False
    assert sample_borrow.extended == True
