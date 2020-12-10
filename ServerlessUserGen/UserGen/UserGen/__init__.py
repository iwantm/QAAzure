import logging
import requests
import uuid
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import azure.functions as func
import json
from os import getenv
import base64


endpoint = getenv("COSMOS_ENDPOINT")
key = getenv("COSMOS_KEY")
client = CosmosClient(endpoint, key)
database_name = 'Users'
database = client.create_database_if_not_exists(id=database_name)
container_name = 'Users'
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/username"),
    offer_throughput=400
)
letters_url = getenv('LETTERS_URL')
numbers_url = getenv('NUMBERS_URL')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    letters = requests.get(letters_url).json()['letters']
    num = requests.get(numbers_url).json()['number']
    username = ''.join(''.join(x) for x in zip(num, letters))
    user = {
        "id": username + str(uuid.uuid4()),
        "username": username
    }
    container.create_item(body=user)

    return func.HttpResponse(
        json.dumps(user)
    )
