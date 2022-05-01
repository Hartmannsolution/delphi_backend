# Models where the entity classes lives. These are sqlalchemy models (not to confuse with pydantic models in schema.py). These are used in the facade class and are created in the main.py class with: models.Base.metadata.create_all(bind=engine)
from sqlalchemy import (
Boolean,
Column,
ForeignKey,
Integer,
String,
)
from sqlalchemy.orm import relationship, Session # Used only for showing commit rollback example
# used for creating OneToMany with foreign keys
from .db import Base                    # imported from sqlalchemy is the class for all entities to inherit

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    class_name = Column(String, ForeignKey("classname.name"))
    is_positive = Column(Boolean) 
    count = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", backref="categories")
    def __repr__(self): # just for testing purpose
        return f'Answer({self.id},{self.text})'

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    answers = relationship("Answer", backref="answers")

class Class_name(Base):
    __tablename__ = "classname"
    name = Column(String, primary_key=True, index=True)
    count = Column(Integer)
    
if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://dev:ax2@db:5432/app', echo=True)
    Base.metadata.drop_all(engine) # remove all tables
    # or drop single table: User.__table__.drop()
    Base.metadata.create_all(engine)

    # commit_entities(engine, Child3(),Parent3())

