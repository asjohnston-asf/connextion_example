from os import environ

import pytest
from botocore.stub import Stubber
from flask_api import status

from hyp3_api import connexion_app, BATCH_CLIENT


@pytest.fixture
def client():
    with connexion_app.app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def batch_stub():
    with Stubber(BATCH_CLIENT) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


def test_submit_job(client, batch_stub):
    batch_stub.add_response(
        'submit_job',
        expected_params={
            'jobName': 'foo',
            'jobQueue': environ['JOB_QUEUE'],
            'jobDefinition': environ['JOB_DEFINITION'],
            'parameters': {'granule': 'foo'}
        },
        service_response={'jobId': 'FAKE_ID_RESPONSE', 'jobName': 'foo'}
    )

    response = client.post('/jobs', json={'granule': 'foo'})
    assert response.status_code == status.HTTP_200_OK
    assert response.get_json() == {
        'jobId': 'FAKE_ID_RESPONSE',
        'jobName': 'foo',
        'parameters': {
            'granule': 'foo',
        },
    }


def test_jobs_bad_method(client):
    response = client.get('/jobs')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.put('/jobs')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.delete('/jobs')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.head('/jobs')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_no_route(client):
    response = client.get('/no/such/path')
    assert response.status_code == status.HTTP_404_NOT_FOUND
