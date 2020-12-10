import logging
from random import randint
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    num = randint(10000, 100000)
    return func.HttpResponse(
        json.dumps({
            'number': str(num)
        })
    )
