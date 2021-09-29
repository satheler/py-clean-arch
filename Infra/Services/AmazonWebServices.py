import boto3

class AmazonWebServices:
  def client(self, service_name: str):
      """ Returns a boto3 client for the specified service."""
      return boto3.client(service_name)
