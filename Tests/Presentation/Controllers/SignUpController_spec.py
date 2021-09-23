import pytest
from Core.Message import Message
from Presentation.Controllers.SignUpController import SignUpController
from Presentation.Errors.ValidationError import ValidationError


def test_when_no_name_is_provided():
    """Should return an ValidationException if no name is provided """
    sut = SignUpController()
    message = Message({
      'email': 'any_email@mail.com',
      'password': 'any_password',
      'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
      sut.handle(message)

    assert {'name': 'is required'} in result.value.errors


def test_when_no_email_is_provided():
    """Should return an ValidationException if no email is provided """
    sut = SignUpController()
    message = Message({
      'name': 'any_name',
      'password': 'any_password',
      'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
      sut.handle(message)

    assert {'email': 'is required'} in result.value.errors

def test_when_no_password_is_provided():
    """Should return an ValidationException if no password is provided """
    sut = SignUpController()
    message = Message({
      'name': 'any_name',
      'email': 'any_email@mail.com',
      'password_confirmation': 'any_password'
    })

    with pytest.raises(ValidationError) as result:
      sut.handle(message)

    assert {'password': 'is required'} in result.value.errors
