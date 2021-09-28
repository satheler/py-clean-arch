import pytest
from pytest_mock import MockerFixture

from Data.Contracts.Encrypter import Encrypter
from Data.UseCases.Account.DatabaseAddAccount import DatabaseAddAccount


def make_encrypter_stub():
    class EncrypterStub(Encrypter):
        def encrypt(self, value: str) -> str:
            return 'hashed_password'

    return EncrypterStub()


def make_sut():
    encrypter_stub = make_encrypter_stub()
    sut = DatabaseAddAccount(encrypter_stub)

    return {
        'sut': sut,
        'encrypter_stub': encrypter_stub
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

    sut.add(
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
        sut.add(
            email=account_data.get('email'),
            password=account_data.get('password')
        )
