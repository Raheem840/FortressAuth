from fastapi import FastAPI  #import FastAPI class from fastapi module. FastAPI is a Python class that provides functionality for your API.
from enum import Enum
app = FastAPI()   #Create an instance of the FastAPI class.

@app.get("/users/me")   #Tells FastAPI that the function right below is in charge of handling requests that go to:#the path / using a get operation
async def read_user_me():
    return {"user_id": "I am the current user!"}   #Return a dictionary with the user_id that was passed in the URL. FastAPI will automatically convert this dictionary to JSON format for the response.


@app.get("/users/{user_id}")   #Tells FastAPI that the function right below is in charge of handling requests that go to:#the path / using a get operation
async def read_user(user_id):
    return {"user_id": user_id}   #Return a dictionary with the user_id that was passed in the URL. FastAPI will automatically convert this dictionary to JSON format for the response.


@app.get("/users/")
async def read_users():
    return ['Rick','Morty','Summer','Beth','Jerry']
#Return a list of users. FastAPI will automatically convert this list to JSON format for the response.

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}