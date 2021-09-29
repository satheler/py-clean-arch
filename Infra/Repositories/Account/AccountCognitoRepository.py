from uuid import uuid4 as uuid
from os import environ

from Infra.Services.AmazonWebServices import AmazonWebServices
from Domain.Entities.Account import Account
from Data.Contracts.StoreAccountRepository import StoreAccountRepository


class AccountCognitoRepository(StoreAccountRepository):
  def store(self, email: str, password: str) -> Account:
      aws = AmazonWebServices()
      client = aws.client('cognito-idp')

      user = client.sign_up(
          ClientId=environ.get('COGNITO_USER_POOL_CLIENT_ID'),
          Username=f'{uuid()}',
          Password=password,
          UserAttributes=[
              {
                  'Name': 'email',
                  'Value': email
              },
          ],
      )

      account = Account()
      account.id = user.get('UserSub')
      account.email = email
      account.password = password

      return account
