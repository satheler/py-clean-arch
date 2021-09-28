from pytest_mock import MockerFixture

from Data.Contracts.Encrypter import Encrypter
from Data.UseCases.Account.DatabaseAddAccount import DatabaseAddAccount


def test_call_encrypter_with_correct_values(mocker: MockerFixture):
  """Should call Encrypter with correct password"""
  class EncrypterStub(Encrypter):
    def encrypt(self, value: str) -> str:
      return 'hashed_password'

  encrypter_stub = EncrypterStub()

  sut = DatabaseAddAccount(encrypter_stub)
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