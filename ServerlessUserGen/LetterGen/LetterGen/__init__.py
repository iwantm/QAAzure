import logging
from random import randint, choice
import string

import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    num = randint(10000, 100000)
    letters = string.ascii_lowercase
    gen = (''.join(choice(letters) for i in range(5)))

    return func.HttpResponse(
        json.dumps({
            'letters': gen
        })
    )
