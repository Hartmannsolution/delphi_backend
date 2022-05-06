# Template for quickly setup a rest api
Sources: 
- [Setup and test with fastAPI and postgres](https://testdriven.io/blog/fastapi-crud/)
- [fastAPI docs](https://fastapi.tiangolo.com/tutorial/path-params/)
- [sql alchemy relationships](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)

## Files
`main.py` is the fastapi main file showing how to make restfull endpoints.
`db.py` is the database setup file that provides 2 classes: `SessionLocal` (for creating session objects) and `Base` for extending with new table classes (ala: Class User(Base):)
`facade.py` has facade methods to showcase how to use methods that get a database session object and data to manipulate the database.
`models.py` contains the sqlalchemy models (the database tables) and shows different cardinalities.
`schemas.py` contains the Pydantic schemas to use for type validation (heavily used in e.g facade.py)
`demo1.py` shows alternative (more low level) ways of using sql without ORM.

## sqlalchemy demo
Simple sql demo in demo1.py and demo using ORM in facade, models and db.py


## Commands
`docker-compose exec db psql --username=dev --dbname=app`: 
`docker inspect fastapi_template_db_1 | grep IPAdd ress`: 
`docker-compose up --build`: Only seems to be able to start up correctly with the --build flag. 
#### postgresql commands
` SELECT column_name FROM information_schema.columns WHERE TABLE_NAME = 'answers';` show all columns in table