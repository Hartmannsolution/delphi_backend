from typing import Optional
from fastapi import  Depends, FastAPI, HTTPException, Request
from app.api import ping
from . import facade, models, schemas
from .db import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# from app.db import engine, database, metadata

app = FastAPI(
    title="delphi_backend",
    version=0.1,
    root_path="/delphi_backend/" # This is for production with nginx forward
)
models.Base.metadata.create_all(bind=engine) # creates all tables that extends the Base class.

# CORS 
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/ip")
def read_root(request: Request):
    client_host = request.client.host
    return {"client_ip": client_host}

# # The order matters: the url path of this fixed resource is the same as the below url with path params (so this static one should come first)
# @app.get("/items/all")
# async def read_user_me(): # async here makes the method superfast asyncronous method. See: https://testdriven.io/blog/fastapi-facade/ for more.
#     return {"all": "show all the items here ..."}

# # Path params
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None): # Type declaration here will ensure that item_id will be parsed as an int and a nicely formatted error message is returned if we try to put text in the parameter on the url request.
#     return {"item_id": item_id, "q": q}

# # Using enums for parameters makes the documentation show legitimate options
# from enum import Enum

# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     print(model_name)
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!!!!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

# # FROM OTHER FILES: route served from file. api/ping.py by using fastapi.APIRouter
# app.include_router(ping.router)

# USING ORM WITH SQLALCHEMY
# Dependency: We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
def get_db():
    db = SessionLocal() # SessionLocal from db module contains the sqlalchemy engine.
    try:
        yield db
    finally:
        db.close()

# These methods can not use async (since it is not supported by sqlalchemy)
# CREATE
# @app.post("/answer/", response_model=schemas.AnswerBase)
# def create_answer(answer: schemas.AnswerBase, db: Session = Depends(get_db)):
#     return facade.create_answer(db=db, answer=answer)

# CREATE MULTIPLE
@app.post("/answers/", response_model=str)
def create_answers(answers: list[schemas.AnswerBase], db: Session = Depends(get_db)):
    for answer in answers:
        if not facade.is_valid_class(db, answer.class_name):
            return "NOT APPROVED - WRONG CLASSNAME"
        ans = facade.create_answer(db=db, answer=answer)
        
    if len(answers)<6:
        return "INSUFFICIENT" # if you have not posted 6 answers you will not be allowed to rate
    return "APPROVED"

@app.post("/answers/rating", response_model=str)
def rate_answers(answers: list[schemas.AnswerRate], db: Session = Depends(get_db)):
    counter = 0
    for answer in answers:
        counter =+ answer.inc_number
        if counter > len(answers): # only allow 10 ratings pr. person
            return "RATED TOO MANY"
        ans = facade.increment_answer(db, answer.id, number=answer.inc_number)
        if ans is None:
            print("Not found")
    return "RATED"

@app.post("/answers/comment", response_model=str)
def comment_answer(answers: list[schemas.AnswerComment],db: Session = Depends(get_db)): 
    for answer in answers:
        ans = facade.comment_answer(db, answer.id, comment=answer.comment)
        if ans is None:
            print("Not found")
    return "COMMENTED"

# READ ALL
@app.get("/answers/{class_name}", response_model=list[schemas.AnswerComment])
def read_users(class_name:str, db: Session = Depends(get_db)):
    answers = facade.get_answers_by_class(db, class_name)
    return answers

@app.post("/classname", response_model=schemas.ClassName)
def create_class(class_name:schemas.ClassName, db: Session = Depends(get_db)):
    result = facade.create_class(db=db, class_name=class_name) # important here to use named parameters.
    return result

@app.get("/classname/{class_name}", response_model=bool)
def is_valid_class(class_name: str, db: Session = Depends(get_db)):
    return facade.is_valid_class(db, class_name)

# # READ BY ID
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = facade.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# # CREATE ITEM ON USER
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return facade.create_user_item(db=db, item=item, user_id=user_id)

# # READ ALL
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = facade.get_items(db, skip=skip, limit=limit)
#     return items
