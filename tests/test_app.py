import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json['service'] == 'flask-devops-demo'

def test_healthz(client):
    res = client.get('/healthz')
    assert res.status_code == 200
    assert res.json['status'] == 'healthy'

def test_add_todo(client):
    res = client.post('/api/v1/todos', json={"task": "Run Automated Tests"})
    assert res.status_code == 201
    assert res.json['item']['task'] == "Run Automated Tests"

