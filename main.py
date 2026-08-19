from fastapi import Depends, FastAPI, HTTPException, Query #import FastAPI class from fastapi module. FastAPI is a Python class that provides functionality for your API.
from enum import Enum
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

app = FastAPI()   #Create an instance of the FastAPI class

@app.get("/health")
async def read_health():
    return {"status": "healthy"}

class User(SQLModel, table=True): #Pydantic model for the user table in the database.
    id : int | None = Field(default=None, primary_key=True)
    email : str = Field(index=True,unique=True)
    hashed_password : str
    
sqlite_file_name = "fortressauth.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"    

engine = create_engine(sqlite_url, echo=True) #The engine holds the connection to the database

def create_db_and_tables(): #Create the database and tables if they don't exist
    SQLModel.metadata.create_all(engine)
    
def get_session():              #The session stores the objects in memory and keeps track of changes made to them, then communicates to the database
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]#Add session dependency to the endpoint function allowing it to access the database session.



@app.on_event("startup") #Create database tables on startup
def on_startup():
    create_db_and_tables()


class UserCreate(BaseModel):#JSON model for user registration data
    email:str
    password:str
    confirm_password:str
    

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#This uses the bcrypt hashing algorithm to encrypt password

@app.post("/register")
def register_user(user_data: UserCreate, session:SessionDep):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed_password = password_context.hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    session.refresh(new_user)
    
    return {"message":"User registered successfully", "user_id": new_user.id, "email": new_user.email}
  
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

