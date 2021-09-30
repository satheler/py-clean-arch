import pytest
from pytest_mock import MockerFixture

from Data.Contracts.StoreAccountRepository import StoreAccountRepository
from Data.UseCases.Account.IdentityProviderStoreAccount import IdentityProviderStoreAccount
from Domain.Entities.Account import Account


@pytest.fixture
def store_account_repository_stub() -> StoreAccountRepository:
    class StoreAccountRepositoryStub(StoreAccountRepository):
        def store(self, email: str, password: str) -> Account:
            account = Account()
            account.id = 'valid_id'
            account.email = 'valid@mail.com'
            account.password = 'valid_password'

            return account

    return StoreAccountRepositoryStub()


@pytest.fixture
def sut(store_account_repository_stub: StoreAccountRepository) -> IdentityProviderStoreAccount:
    return IdentityProviderStoreAccount(store_account_repository_stub)


def test_call_store_account_repository_with_correct_values(
    sut: IdentityProviderStoreAccount,
    store_account_repository_stub: StoreAccountRepository,
    mocker: MockerFixture
):
    """Should call StoreAccountRepository with correct values"""
    store_account_repository_spy = mocker.spy(
        store_account_repository_stub, 'store')

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
        password='valid_password',
    )


def test_raise_when_store_account_repository_raises(
    sut: IdentityProviderStoreAccount,
    store_account_repository_stub: StoreAccountRepository,
    mocker: MockerFixture
) -> None:
    """Should raise if StoreAccountRepository raises"""
    store_account_repository_spy = mocker.spy(
        store_account_repository_stub, 'store')
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


def test_on_success(sut: IdentityProviderStoreAccount):
    """Should return an Account on success"""
    account_data = {
        'email': 'valid@mail.com',
        'password': 'valid_password'
    }

    account = sut.store(
        email=account_data.get('email'),
        password=account_data.get('password')
    )

    assert isinstance(account, Account)
    assert account.id == 'valid_id'
    assert account.email == 'valid@mail.com'
    assert account.password == 'valid_password'
