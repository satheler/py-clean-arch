import boto3
from os import environ

import pytest
from moto import mock_cognitoidp


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    environ['AWS_ACCESS_KEY_ID'] = 'testing'
    environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    environ['AWS_SECURITY_TOKEN'] = 'testing'
    environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def cognito_idp(aws_credentials):
    with mock_cognitoidp():
        client = boto3.client('cognito-idp', region_name='us-east-1')
        
        user_pool = create_user_pool(client)
        user_pool_id = user_pool.get('Id')

        user_pool_client = create_user_pool_client(client, user_pool_id)
        environ['COGNITO_USER_POOL_CLIENT_ID'] = user_pool_client.get('ClientId')
        
        yield client


def create_user_pool(client, pool_name: str = 'testing'):
    user_pool = client.create_user_pool(
        PoolName=pool_name,
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 8,
                'RequireUppercase': False,
                'RequireLowercase': False,
                'RequireNumbers': False,
                'RequireSymbols': False,
                'TemporaryPasswordValidityDays': 7
            }
        },
        AliasAttributes=[
            'email',
        ],
        VerificationMessageTemplate={
            'DefaultEmailOption': 'CONFIRM_WITH_CODE'
        },
        MfaConfiguration='OFF',
        EmailConfiguration={
            'EmailSendingAccount': 'COGNITO_DEFAULT',
        },
        AdminCreateUserConfig={
            'AllowAdminCreateUserOnly': False,
        },
        Schema=[
            {
                'Name': 'name',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False,
                'StringAttributeConstraints': {
                    'MinLength': '0',
                    'MaxLength': '2048'
                }
            },
            {
                'Name': 'nickname',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False,
                'StringAttributeConstraints': {
                    'MinLength': '0',
                    'MaxLength': '2048'
                }
            },
            {
                'Name': 'picture',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False,
                'StringAttributeConstraints': {
                    'MinLength': '0',
                    'MaxLength': '2048'
                }
            },
            {
                'Name': 'email_verified',
                'AttributeDataType': 'Boolean',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False
            },
            {
                'Name': 'updated_at',
                'AttributeDataType': 'Number',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False,
                'NumberAttributeConstraints': {
                    'MinValue': '0'
                }
            },
        ],
        UsernameConfiguration={
            'CaseSensitive': False
        },
    )

    return user_pool.get('UserPool')

def create_user_pool_client(client, user_pool_id: str):
  user_pool_client = client.create_user_pool_client(
    UserPoolId=user_pool_id,
    AccessTokenValidity=60,
    RefreshTokenValidity=30,
    AllowedOAuthFlowsUserPoolClient=False,
    ClientName='testing',
    ExplicitAuthFlows=[
      'ALLOW_CUSTOM_AUTH',
      'ALLOW_REFRESH_TOKEN_AUTH',
      'ALLOW_USER_PASSWORD_AUTH',
      'ALLOW_USER_SRP_AUTH'
    ],
    IdTokenValidity=60,
    GenerateSecret=False,
    PreventUserExistenceErrors='ENABLED',
    TokenValidityUnits={
      'AccessToken': 'minutes',
      'IdToken': 'minutes',
      'RefreshToken': 'days'
    }
  )


  return user_pool_client.get('UserPoolClient')