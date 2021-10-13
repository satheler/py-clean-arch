from Infra.Repositories.Account.AccountCognitoRepository import AccountCognitoRepository
from Data.UseCases.Account.IdentityProviderStoreAccount import IdentityProviderStoreAccount
from Presentation.Controllers.SignUpController import SignUpController
from Utils.EmailValidatorAdapter import EmailValidatorAdapter


def make_sign_up_controller() -> SignUpController:
    email_validator_adapter = EmailValidatorAdapter()
    store_account_repository = AccountCognitoRepository()
    identity_provider_store_account = IdentityProviderStoreAccount(
        store_account_repository=store_account_repository
    )
    return SignUpController(
        email_validator=email_validator_adapter,
        store_account=identity_provider_store_account
    )
