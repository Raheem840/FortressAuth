from fastapi import Depends, FastAPI, HTTPException, Query #import FastAPI class from fastapi module. FastAPI is a Python class that provides functionality for your API.
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

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


class UserLogin(BaseModel):#JSON model for user login data
    email:str
    password:str
    
@app.post("/login")
def login_user(user_data: UserLogin, session:SessionDep):
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=401,detail="Invalid email or password")
    if not password_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    token = create_access_token(data={"sub":user.email}, expires_delta=timedelta(minutes=30))
    
    
    return {"message":"Login successful", "access_token": token, "token_type": "bearer"}
    
    
  
def create_access_token(data:dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
