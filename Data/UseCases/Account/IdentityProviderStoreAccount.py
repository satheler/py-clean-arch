from Domain.UseCases.Account import StoreAccount
from Data.Contracts.StoreAccountRepository import StoreAccountRepository


class IdentityProviderStoreAccount(StoreAccount):
    def __init__(
        self,
        store_account_repository: StoreAccountRepository
    ) -> None:
        self.store_account_repository = store_account_repository

    def store(self, email: str, password: str):
        account = self.store_account_repository.store(
            email=email,
            password=password
        )

        return account
