import re
import pytest
from pytest_mock import MockerFixture

from Utils.EmailValidatorAdapter import EmailValidatorAdapter

@pytest.fixture
def sut() -> EmailValidatorAdapter:
  return EmailValidatorAdapter()

def test_when_invalid_email_is_provided(sut: EmailValidatorAdapter, mocker: MockerFixture):
    """Should return false if email is invalid"""
    mocker.patch.object(sut, 'is_valid', return_value=False)

    is_valid = sut.is_valid('invalid_email@mail.com')
    assert is_valid == False


def test_when_valid_email_is_provided(sut: EmailValidatorAdapter, mocker: MockerFixture):
    """Should return true if email is valid"""
    mocker.patch.object(sut, 'is_valid', return_value=True)

    is_valid = sut.is_valid('valid_email@mail.com')
    assert is_valid == True


def test_call_regex_match(sut: EmailValidatorAdapter, mocker: MockerFixture):
    """Should return true if email is valid"""
    re_spy = mocker.spy(re, 'match')

    email = 'valid_email@mail.com'

    sut.is_valid(email)
    re_spy.assert_called_once_with('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', email)
