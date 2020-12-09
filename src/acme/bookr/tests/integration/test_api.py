#  __copyright__ = "Copyright (c) 2020 Gordon Elliott"

import pytest
import requests

HOST = "localhost"
PORT = 5000

BOOK_REQUESTERS = (
    dict(
        email="jb@example.com",
        title="Of Mice and Men",
    ),
    dict(
        email="op@example.com",
        title="Of Mice and Men",
    ),
    dict(
        email="jb@example.com",
        title="The Old Man and the Sea",
    ),
    dict(
        email="bob@woodward.name",
        title="The Grapes of Wrath",
    ),
)


@pytest.fixture(scope='function')
def sample_requests():
    samples = [
        requests.post(f"http://{HOST}:{PORT}/request", sample_dict).json()
        for sample_dict in BOOK_REQUESTERS
    ]
    samples_by_id = {
        sample["id"]: sample for sample in samples
    }
    yield samples_by_id

    # teardown
    for sample in samples:
        requests.delete(f"http://{HOST}:{PORT}/request/{sample['id']}")


def test_request_post():
    response = requests.post(
        f"http://{HOST}:{PORT}/request",
        dict(
            email="jb@example.com",
            title="Of Mice and Men",
        )
    )

    assert response.status_code == 200
    deserialized = response.json()
    assert deserialized['email'] == "jb@example.com"
    assert deserialized['title'] == "Of Mice and Men"

    # clean up
    requests.delete(f"http://{HOST}:{PORT}/request/{deserialized['id']}")


def test_request_post_bad_email():
    response = requests.post(
        f"http://{HOST}:{PORT}/request",
        dict(
            email="jb@example_com",
            title="Of Mice and Men",
        )
    )

    assert response.status_code == 400


def test_request_get_all(sample_requests):
    response = requests.get(f"http://{HOST}:{PORT}/request")

    assert response.status_code == 200
    deserialized = response.json()

    assert len(deserialized) == len(sample_requests)
    for request_dict in deserialized:
        assert request_dict == sample_requests[request_dict["id"]]


def test_request_get_exists(sample_requests):
    sample_id, *_ = sample_requests.keys()
    response = requests.get(f"http://{HOST}:{PORT}/request/{sample_id}")

    assert response.status_code == 200
    deserialized = response.json()

    assert deserialized == sample_requests[sample_id]


def test_request_get_missing(sample_requests):
    non_existant_id = "not an id"
    response = requests.get(f"http://{HOST}:{PORT}/request/{non_existant_id}")

    assert response.status_code == 404
    with pytest.raises(requests.exceptions.HTTPError):
        response.raise_for_status()


def test_request_delete_exists(sample_requests):
    _, sample_id, *__ = sample_requests.keys()
    response = requests.delete(f"http://{HOST}:{PORT}/request/{sample_id}")

    assert response.status_code == 200


def test_request_delete_missing(sample_requests):
    non_existant_id = "not an id"
    response = requests.delete(f"http://{HOST}:{PORT}/request/{non_existant_id}")

    assert response.status_code == 200
