from fastapi import FastAPI  #import FastAPI class from fastapi module. FastAPI is a Python class that provides functionality for your API.
from enum import Enum
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()   #Create an instance of the FastAPI class.

@app.get("/health")
async def read_health():
    return {"status": "healthy"}

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    email : str = Field(index=True,unique=True)
    hashed_password : str
    
sqlite_file_name = "fortressauth.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"    

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    create_db_and_tables()
  
  
#class ModelName(str, Enum):
    #lexnet = "alexnet"
    #resnet = "resnet"
    #lenet = "lenet"
#@app.get("/models/{model_name}")
#async def get_model(model_name: ModelName):
    #if model_name is ModelName.alexnet:
     #   return {"model_name": model_name, "message": "Deep Learning FTW!"}
    #if model_name.value == "lenet":
    #    return {"model_name": model_name, "message": "LeCNN all the images"}
    #return {"model_name": model_name, "message": "Have some residuals"}

