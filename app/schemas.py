# pydantic models to use for type checking.
from typing import  Optional
from pydantic import BaseModel

class AnswerBase(BaseModel):
    text: str
    class_name: str
    is_positive: bool
    class Config: # this is to let pydantic know how this should be interpreted (as a dict i believe). https://stackoverflow.com/questions/69504352/fastapi-get-request-results-in-typeerror-value-is-not-a-valid-dict.
        orm_mode = True

class Answer(AnswerBase):
    id: int
    count: int
    def __repr__(self):
        return 'answer: '+id

class AnswerRate(Answer):
    inc_number: int

class AnswerCollection(BaseModel):
    answers: list[AnswerBase]

class CategoryBase(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True

class Category(CategoryBase):
    id: int
    answers: list[Answer] = [] # valid from python 3.9
    def __repr__(self):
        return 'category: '+id
    
class ClassNameBase(BaseModel):
    name: str
    count: int = 0
    class Config:
        orm_mode = True #to avoid error: value is not a valid dict (type=type_error.dict)

class ClassName(ClassNameBase):
    logins: list[str] = []
