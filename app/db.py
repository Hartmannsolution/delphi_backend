from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL, # connect_args={"check_same_thread": False} # only for sqllite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # class for making session objects.
Base = declarative_base() # The base class to be extended by all future entity classes / Models.