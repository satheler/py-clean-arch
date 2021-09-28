from Domain.UseCases.Account import StoreAccount
from Data.Contracts.StoreAccountRepository import StoreAccountRepository
from Data.Contracts.Encrypter import Encrypter


class IdentityProviderStoreAccount(StoreAccount):
    def __init__(
        self,
        encrypter: Encrypter,
        store_account_repository: StoreAccountRepository
    ) -> None:
        self.store_account_repository = store_account_repository
        self.encrypter = encrypter

    def store(self, email: str, password: str):
        hashed_password = self.encrypter.encrypt(password)
        self.store_account_repository.store(
            email=email,
            password=hashed_password
        )
        
         
