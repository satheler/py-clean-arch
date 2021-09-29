import pytest

from Infra.Repositories.Account.AccountCognitoRepository import AccountCognitoRepository
from Domain.Entities.Account import Account

@pytest.fixture
def sut() -> AccountCognitoRepository:
    return AccountCognitoRepository()

def test_on_success(sut: AccountCognitoRepository, cognito_idp):
    """Should return an Account on success"""
    email = 'valid@mail.com'
    password = 'hashed_password'

    account = sut.store(email, password)

    assert isinstance(account, Account)
    assert account.id is not None
    assert account.email is not None
    assert account.password is not None