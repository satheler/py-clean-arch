from os import environ

import boto3


class AmazonWebServices:
    def client(self, service_name: str):
        """ Returns a boto3 client for the specified service."""
        return boto3.client(
            service_name,
            region_name=environ.get('AWS_REGION'),
            endpoint_url=environ.get('AWS_ENDPOINT_URL'),
        )
