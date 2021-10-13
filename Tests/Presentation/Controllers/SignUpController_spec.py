import pytest
from pytest_mock import MockerFixture

from Domain.Entities.Account import Account
from Domain.UseCases.Account import StoreAccount

from Presentation.Adapters.Message import Message
from Presentation.Controllers.SignUpController import SignUpController
from Presentation.Errors.ValidationError import ValidationError

from Validators.Contracts.EmailValidator import EmailValidator

fake_account = {
    'id': 'valid_id',
    'email': 'valid_email@mail.com',
    'password': 'valid_password'
}


@pytest.fixture
def email_validator_stub() -> EmailValidator:
    class EmailValidatorStub(EmailValidator):
        def is_valid(self, email: str) -> bool:
            return True

    return EmailValidatorStub()


@pytest.fixture
def store_account_stub() -> StoreAccount:
    class StoreAccountStub(StoreAccount):
        def store(self, email: str, password: str) -> Account:
            return fake_account

    return StoreAccountStub()


@pytest.fixture
def sut(email_validator_stub: EmailValidator, store_account_stub: StoreAccount) -> SignUpController:
    return SignUpController(email_validator_stub, store_account_stub)


def test_when_no_email_is_provided(sut: SignUpController) -> None:
    """Should return a ValidationException if no email is provided """
    message = Message({
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'email': 'is required'} in result.value.errors


def test_when_no_password_is_provided(sut: SignUpController) -> None:
    """Should return a ValidationException if no password is provided """
    message = Message({
        'email': 'any_email@mail.com',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'password': 'is required'} in result.value.errors


def test_when_no_password_confirmation_is_provided(sut: SignUpController) -> None:
    """Should return a ValidationException if no password_confirmation is provided """
    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {'password_confirmation': 'is required'} in result.value.errors


def test_when_password_confirmation_fails(sut: SignUpController) -> None:
    """Should return a ValidationException if password_confirmation is different from password"""
    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'invalid_password'
    })

    with pytest.raises(ValidationError) as result:
        sut.handle(message)

    assert {
        'password_confirmation': 'does not match with password'} in result.value.errors


def test_when_invalid_email_is_provided(
    sut: SignUpController,
    email_validator_stub: EmailValidator,
    mocker: MockerFixture
) -> None:
    """Should return a ValidationException if an invalid email is provided"""
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


def test_call_email_validator_with_correct_values(
    sut: SignUpController,
    email_validator_stub: EmailValidator,
    mocker: MockerFixture
) -> None:
    """Should call EmailValidator with correct email"""
    email_validator_spy = mocker.spy(email_validator_stub, 'is_valid')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    sut.handle(message)

    email_validator_spy.assert_called_once_with(message.content.get('email'))


def test_raise_when_email_validator_raises(
    sut: SignUpController,
    email_validator_stub: EmailValidator,
    mocker: MockerFixture
) -> None:
    """Should raise if EmailValidator raises"""
    email_validator_spy = mocker.spy(email_validator_stub, 'is_valid')
    email_validator_spy.side_effect = Exception('Unexpected error')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(BaseException):
        sut.handle(message)


def test_call_store_account_with_correct_values(
    sut: SignUpController,
    store_account_stub: StoreAccount,
    mocker: MockerFixture
) -> None:
    """Should call StoreAccount with correct values"""
    store_account_spy = mocker.spy(store_account_stub, 'store')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    sut.handle(message)

    store_account_spy.assert_called_once_with(
        email=message.content.get('email'),
        password=message.content.get('password')
    )


def test_raise_when_store_account_raises(
    sut: SignUpController,
    store_account_stub: StoreAccount,
    mocker: MockerFixture
) -> None:
    """Should raise if StoreAccount raises"""
    store_account_spy = mocker.spy(store_account_stub, 'store')
    store_account_spy.side_effect = Exception('Unexpected error')

    message = Message({
        'email': 'any_email@mail.com',
        'password': 'any_password',
        'password_confirmation': 'any_password'
    })

    with pytest.raises(BaseException):
        sut.handle(message)


def test_on_success(sut: SignUpController) -> None:
    """Should return an Account if correct values are provided"""
    message = Message({
        'email': 'valid_email@mail.com',
        'password': 'valid_password',
        'password_confirmation': 'valid_password'
    })

    result = sut.handle(message)

    assert fake_account == result
