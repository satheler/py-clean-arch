import pytest
from pytest_mock import MockerFixture

from Data.Contracts.Encrypter import Encrypter
from Data.Contracts.StoreAccountRepository import StoreAccountRepository
from Data.UseCases.Account.IdentityProviderStoreAccount import IdentityProviderStoreAccount
from Domain.Entities.Account import Account


def make_encrypter_stub():
    class EncrypterStub(Encrypter):
        def encrypt(self, value: str) -> str:
            return 'hashed_password'

    return EncrypterStub()


def make_store_account_repository_stub():
  class StoreAccountRepositoryStub(StoreAccountRepository):
    def store(self, email: str, password: str) -> Account:
      account = Account()
      account.id = 'valid_id'
      account.email = 'valid@mail.com'
      account.password = 'hashed_password'

      return account

  return StoreAccountRepositoryStub()

def make_sut():
    encrypter_stub = make_encrypter_stub()
    store_account_repository_stub = make_store_account_repository_stub()
    sut = IdentityProviderStoreAccount(encrypter_stub, store_account_repository_stub)

    return {
        'sut': sut,
        'encrypter_stub': encrypter_stub,
        'store_account_repository_stub': store_account_repository_stub
    }


def test_call_encrypter_with_correct_values(mocker: MockerFixture):
    """Should call Encrypter with correct password"""
    test = make_sut()
    sut = test.get('sut')
    encrypter_stub = test.get('encrypter_stub')

    encrypter_spy = mocker.spy(encrypter_stub, 'encrypt')

    account_data = {
        'email': 'valid@mail.com',
        'password': 'valid_password'
    }

    sut.store(
        email=account_data.get('email'),
        password=account_data.get('password')
    )

    encrypter_spy.assert_called_once_with('valid_password')


def test_raise_when_encrypter_raises(mocker: MockerFixture) -> None:
    """Should raise if Encrypter raises"""
    test = make_sut()
    sut = test.get('sut')
    encrypter_stub = test.get('encrypter_stub')

    encrypter_spy = mocker.spy(encrypter_stub, 'encrypt')
    encrypter_spy.side_effect = Exception('Unexpected error')

    account_data = {
        'email': 'valid@mail.com',
        'password': 'valid_password'
    }

    with pytest.raises(BaseException):
        sut.store(
            email=account_data.get('email'),
            password=account_data.get('password')
        )

def test_call_store_account_repository_with_correct_values(mocker: MockerFixture):
    """Should call StoreAccountRepository with correct values"""
    test = make_sut()
    sut = test.get('sut')
    store_account_repository_stub = test.get('store_account_repository_stub')

    store_account_repository_spy = mocker.spy(store_account_repository_stub, 'store')

    account_data = {
        'email': 'valid@mail.com',
        'password': 'valid_password'
    }

    sut.store(
        email=account_data.get('email'),
        password=account_data.get('password')
    )

    store_account_repository_spy.assert_called_once_with(
        email=account_data.get('email'),
        password='hashed_password',
    )

def test_raise_when_store_account_repository_raises(mocker: MockerFixture) -> None:
    """Should raise if StoreAccountRepository raises"""
    test = make_sut()
    sut = test.get('sut')
    store_account_repository_stub = test.get('store_account_repository_stub')

    store_account_repository_spy = mocker.spy(store_account_repository_stub, 'store')
    store_account_repository_spy.side_effect = Exception('Unexpected error')

    account_data = {
        'email': 'valid@mail.com',
        'password': 'valid_password'
    }

    with pytest.raises(BaseException):
        sut.store(
            email=account_data.get('email'),
            password=account_data.get('password')
        )