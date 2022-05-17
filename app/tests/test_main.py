# Purpose here is to show how easy we make re`tassured type tests in python. Run: `docker-compose exec web pytest .`
# from starlette.testclient import TestClient
from fastapi.testclient import TestClient # https://fastapi.tiangolo.com/tutorial/testing/

# from starlette.requests import Request
# from starlette.responses import Response
import json

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_new_classname():
    test_request_payload = {"name":"testclassabc"}
    response = client.post("/classname", data=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == None or { "name": "testclassabc", "count": 0, "logins": [] } # If classname exist we get None back from the endpoint.
