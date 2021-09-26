import pytest
from Utils.EmailValidatorAdapter import EmailValidatorAdapter

def test_when_invalid_email_is_provided():
  """Should return false if email is invalid"""
  sut = EmailValidatorAdapter()
  is_valid = sut.is_valid('invalid_email@mail.com')
  assert is_valid == False