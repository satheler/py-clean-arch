from typing import Dict

import pytest
from pytest_mock import MockerFixture

from Contracts import EmailValidator
from Core.Message import Message

from Domain.Entities.Account import Account
from Domain.UseCases.Account import AddAccount

from Presentation.Controllers.SignUpController import SignUpController
from Presentation.Errors.ValidationError import ValidationError


def make_email_validator_stub() -> EmailValidator:
    class EmailValidatorStub(EmailValidator):
        def is_valid(self, email: str) -> bool:
            return True

    return EmailValidatorStub()


fake_account = {
    'id': 'valid_id',
    'email': 'valid_email@mail.com',
    'password': 'valid_password'
}


def make_add_account_stub() -> AddAccount:
    class AddAccountStub(AddAccount):
        def add(self, email: str, password: str) -> Account:
            return fake_account

    return AddAccountStub()


def make_sut() -> Dict[str, object]:
    email_validator_stub = make_email_validator_stub()
    add_account_stub = make_add_account_stub()
    sut = SignUpController(email_validator_stub, add_account_stub)

    return {
        'sut': sut,
        'email_validator_stub': email_validator_stub,
        'add_account_stub': add_account_stub
    }


def test_when_no_email_is_provided() -> None:
    """Should return a ValidationException if no email is provided """
    test = make_sut()
    sut = test.get('sut')

    message = Message({
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'email': 'is required'} in result.value.errors


def test_when_no_password_is_provided() -> None:
    """Should return a ValidationException if no password is provided """
    test = make_sut()
    sut = test.get('sut')

    message = Message({
        'email': 'any_email@mail.com',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'password': 'is required'} in result.value.errors


def test_when_no_password_confirmation_is_provided() -> None:
    """Should return a ValidationException if no password_confirmation is provided """
    test = make_sut()
    sut = test.get('sut')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'password_confirmation': 'is required'} in result.value.errors


def test_when_password_confirmation_fails() -> None:
    """Should return a ValidationException if password_confirmation is different from password"""
    test = make_sut()
    sut = test.get('sut')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'invalid_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {
        'password_confirmation': 'does not match with password'} in result.value.errors


def test_when_invalid_email_is_provided(mocker: MockerFixture) -> None:
    """Should return a ValidationException if an invalid email is provided"""
    test = make_sut()
    sut = test.get('sut')
    email_validator_stub = test.get('email_validator_stub')

    mocker.patch.object(email_validator_stub, 'is_valid',
                        return_value=False, autospec=True)

    message = Message({
        'email': 'invalid_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'email': 'is invalid'} in result.value.errors


def test_call_email_validator_with_correct_values(mocker: MockerFixture) -> None:
    """Should call EmailValidator with correct email"""
    test = make_sut()
    sut = test.get('sut')
    email_validator_stub = test.get('email_validator_stub')

    email_validator_spy = mocker.spy(email_validator_stub, 'is_valid')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    sut.handle(message)

    email_validator_spy.assert_called_once_with(message.body.get('email'))


def test_raise_when_email_validator_raises(mocker: MockerFixture) -> None:
    """Should raise if EmailValidator raises"""
    test = make_sut()
    sut = test.get('sut')
    email_validator_stub = test.get('email_validator_stub')

    email_validator_spy = mocker.spy(email_validator_stub, 'is_valid')
    email_validator_spy.side_effect = Exception('Unexpected error')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(BaseException):
        sut.handle(message)


def test_call_add_account_with_correct_values(mocker: MockerFixture) -> None:
    """Should call AddAccount with correct values"""
    test = make_sut()
    sut = test.get('sut')
    add_account_stub = test.get('add_account_stub')

    add_account_spy = mocker.spy(add_account_stub, 'add')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    sut.handle(message)

    add_account_spy.assert_called_once_with(
        email=message.body.get('email'),
        password=message.body.get('password')
    )


def test_raise_when_add_account_raises(mocker: MockerFixture) -> None:
    """Should raise if AddAccount raises"""
    test = make_sut()
    sut = test.get('sut')
    add_account_stub = test.get('add_account_stub')

    add_account_spy = mocker.spy(add_account_stub, 'add')
    add_account_spy.side_effect = Exception('Unexpected error')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(BaseException):
        sut.handle(message)


def test_when_account_is_created(mocker: MockerFixture) -> None:
    """Should return an Account if correct values are provided"""
    test = make_sut()
    sut = test.get('sut')

    message = Message({
        'email': 'valid_email@mail.com',
        'password': 'valid_password',
        'password_confirmation': 'valid_password'
    })

    result = sut.handle(message)

    assert fake_account == result
