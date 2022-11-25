from fastapi import FastAPI
from enum import Enum
import os


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


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

    
app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello world"}


@app.get('/items/{item_id}')
async def get_item(item_id: int):
    response = {
        "item_id": item_id,
        "value": data[item_id]
    }

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
    
@app.get('/resource/{file_path:path}')
async def get_resource(file_path: str, limit: int = 3):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        result = {}
        
        counter = 0
        for row in file_content.split('\n'):
            if counter >= limit:
                break

            data = row.split(':')

            name = data[0]
            points = int(data[1])

            result[name] = points
            
            counter += 1

        return result
    else:
        return {"file_content": None}
    
