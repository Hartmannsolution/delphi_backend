# Template for quickly setup a rest api
Sources: 
- [Setup and test with fastAPI and postgres](https://testdriven.io/blog/fastapi-crud/)
- [fastAPI docs](https://fastapi.tiangolo.com/tutorial/path-params/) and [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
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

## Test
With pytest and requests installed (requirements.txt) we can easily run restassured type tests. See app/tests/test_main.py for example. Run with `docker-compose exec web pytest .`
See more on [FastApi Documentation](https://fastapi.tiangolo.com/tutorial/testing/)

## Deploy
In main.py comment out this line: `root_path="/delphi_backend/" # This is for production with nginx forward` when running locally and bring it back before git push.
On the server `sshedu` go to directory: delphi_backend and `git pull` to get the newest changes. No need to restart container or do anything. In the docker compose it says restart on changes.