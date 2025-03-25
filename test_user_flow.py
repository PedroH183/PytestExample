import library_management_system as library


def test_can_borrow(sample_user):
    """ Quando o usuário pode pegar emprestado, então o status deve ser atualizado corretamente """

    assert sample_user.can_borrow() == True

def test_dont_can_borrow(sample_user):
    """ Quando o usuário não pode pegar emprestado, então o status deve ser atualizado corretamente """

    # sample_user has borrowed books more than 2
    sample_user.borrowed_books = ['1', '2', '3', '4'] # max allow is 3
    assert sample_user.can_borrow() == False

    sample_user.borrowed_books = []

    # sample_user is deactivated
    sample_user.deactivate()
    assert sample_user.can_borrow() == False

    # sample_user is deactivated and has borrowed books more than 3
    sample_user.borrowed_books = ['1', '2', '3']
    assert sample_user.can_borrow() == False

def test_to_dict(sample_user):
    """ Quando o usuário é convertido em dicionário, então os atributos devem ser convertidos corretamente """

    user_dict = sample_user.to_dict()
    assert 'id' in user_dict
    assert user_dict['name'] == "João Silva"
    assert user_dict['email'] == "joao_silva@teste.com.br"
    assert user_dict['role'] == library.UserRole.MEMBER.value
    assert user_dict['borrowed_books'] == []
    assert user_dict['active'] == True

def test_reactivate_user(sample_user):
    """ Quando o usuário é reativado, então o status deve ser atualizado corretamente """

    sample_user.deactivate()
    assert sample_user.active == False

    sample_user.reactivate()
    assert sample_user.active == True


