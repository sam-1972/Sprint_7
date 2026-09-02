import pytest

from api_methods import CourierApi, OrderApi
from helpers import generate_courier_data


@pytest.fixture
def courier_data():
    data = generate_courier_data()
    yield data

    login_data = {
        'login': data['login'],
        'password': data['password'],
    }
    login_response = CourierApi.login_courier(login_data)

    if login_response.status_code == 200:
        courier_id = login_response.json()['id']
        CourierApi.delete_courier(courier_id)


@pytest.fixture
def registered_courier(courier_data):
    response = CourierApi.create_courier(courier_data)

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
        OrderApi.cancel_order(track)
