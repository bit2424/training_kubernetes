import pytest
import mock
import connexion
from src import launch


@pytest.fixture(scope='module')
def client():
    flask_app = connexion.FlaskApp(__name__)
    with flask_app.app.test_client() as c:
        yield c

@pytest.fixture()
def user_role():
    return 'collaborator'

def test_get_health(client):
    # GIVEN no query parameters or payload
    # WHEN I access to the url GET /health
    # THEN the HTTP response is 404 not found
    response = client.get('/health')
    assert response.status_code == 404

