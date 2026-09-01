import allure
import pytest
import requests

from config import REQUEST_TIMEOUT
from data import ResponseMessages
from endpoints import Endpoints
from urls import Urls


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно успешно создать')
    def test_create_courier_success(self, courier_data):
        with allure.step('Отправить запрос на создание курьера'):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
                json=courier_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и тело ответа'):
            assert response.status_code == 201
            assert response.json() == {'ok': True}

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_returns_error(
        self,
        courier_data,
    ):
        with allure.step('Создать первого курьера'):
            first_response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
                json=courier_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Повторно отправить те же данные'):
            second_response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
                json=courier_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и сообщение об ошибке'):
            assert first_response.status_code == 201
            assert second_response.status_code == 409
            assert (
                ResponseMessages.DUPLICATE_COURIER
                in second_response.json()['message']
            )

    @allure.title(
        'Нельзя создать курьера без обязательного поля: {missing_field}'
    )
    @pytest.mark.parametrize(
        'missing_field',
        ['login', 'password'],
        ids=['without_login', 'without_password'],
    )
    def test_create_courier_without_required_field_returns_error(
        self,
        courier_data,
        missing_field,
    ):
        incomplete_data = courier_data.copy()
        incomplete_data.pop(missing_field)

        with allure.step(
            f'Отправить запрос без поля {missing_field}'
        ):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
                json=incomplete_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и сообщение об ошибке'):
            assert response.status_code == 400
            assert (
                ResponseMessages.CREATE_COURIER_MISSING_DATA
                in response.json()['message']
            )
