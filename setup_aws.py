from os import environ
from dotenv import load_dotenv

import boto3

from conftest import create_user_pool, create_user_pool_client

load_dotenv()

environ['AWS_ACCESS_KEY_ID'] = 'testing'
environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
environ['AWS_SECURITY_TOKEN'] = 'testing'
environ['AWS_SESSION_TOKEN'] = 'testing'

print(environ)

client = boto3.client(
    'cognito-idp',
    region_name=environ.get('AWS_REGION'),
    endpoint_url=environ.get('AWS_ENDPOINT_URL')
)

user_pool = create_user_pool(client)
user_pool_id = user_pool.get('Id')

user_pool_client = create_user_pool_client(client, user_pool_id)
print(user_pool_client.get('ClientId'))
