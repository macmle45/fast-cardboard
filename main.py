from fastapi import FastAPI, Query
from enum import Enum
import os
from typing import Union
from random import randint

from request_body import Item


# sample dict data
data = {
    0: "Hello",
    1: "How are you?",
    2: "Nice to meet you"
}

users = {
    'me': 'John',
    0: 'Jane',
    1: 'Victor'
}


# enum class with str type
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

    
app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello world"}


@app.get('/item/{item_id}')
async def get_item(item_id: int, q: str | None = Query(default=None, min_length=3, max_length=10)):
    response = {
        "item_id": item_id,
        "value": data[item_id]
    }

    if q:
        response['q'] = q

    return response


@app.get('/users/me')
async def get_my_user():
    response = {
        "user_id": 'me',
        "name": users['me']
    }

    return response


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    response = {
        "user_id": user_id,
        "name": users[user_id]
    }

    return response

# using Enum
@app.get('/models/{model_name}')
async def get_models(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }
    if model_name.value == 'lenet':
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }
    
    return {
            "model_name": model_name,
            "message": "Have some residuals"
        }


@app.get('/files/{file_path:path}')
async def get_files(file_path: str):    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()
    
        return {
                "file_path": file_path,
                "file_content": file_content
                }
    
    else:
        return {"file_content": None}


"""
file_path: str - path parameter
limit: int - required query parameter
skip: int = 0 - default query parameter
random_item: bool | None = None - optional query parameter
"""
@app.get('/resource/{file_path:path}')
async def get_resource(file_path: str, limit: int, skip: int = 0, random_item: Union[bool, None] = None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        content = file_content.split('\n')[skip:limit]
        result = {}

        if random_item:
            random_content_item = randint(skip, limit)
            data = content[random_content_item].split(':')

            name = data[0]
            points = int(data[1])

            result[name] = points

            return result
        
        for row in content:
            data = row.split(':')

            name = data[0]
            points = int(data[1])

            result[name] = points
            

        return result
    else:
        return {"file_content": None}
    

@app.post('/items/')
async def create_item(item: Item):
    result = {
        'name': item.name,
        'price': item.price,
    }

    if item.tax:
        result['tax'] = item.tax
        result['price_tax_incl'] = item.price + (item.tax / 100 * item.price)
    
    return result
