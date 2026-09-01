import pytest
import requests

from config import REQUEST_TIMEOUT
from endpoints import Endpoints
from helpers import generate_courier_data
from urls import Urls


@pytest.fixture
def courier_data():
    data = generate_courier_data()
    yield data

    login_response = requests.post(
        f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
        json={
            'login': data['login'],
            'password': data['password'],
        },
        timeout=REQUEST_TIMEOUT,
    )
    if login_response.status_code == 200:
        courier_id = login_response.json()['id']
        requests.delete(
            f'{Urls.BASE_URL}'
            f'{Endpoints.DELETE_COURIER}{courier_id}',
            timeout=REQUEST_TIMEOUT,
        )


@pytest.fixture
def registered_courier(courier_data):
    response = requests.post(
        f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
        json=courier_data,
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code != 201:
        pytest.fail(
            'Не удалось создать курьера для предусловия теста: '
            f'{response.status_code} {response.text}'
        )
    return courier_data


@pytest.fixture
def created_order_tracks():
    tracks = []
    yield tracks

    for track in tracks:
        requests.put(
            f'{Urls.BASE_URL}{Endpoints.CANCEL_ORDER}',
            params={'track': track},
            timeout=REQUEST_TIMEOUT,
        )
