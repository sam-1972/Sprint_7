import allure
import pytest
import requests

from config import REQUEST_TIMEOUT
from data import ResponseMessages
from endpoints import Endpoints
from helpers import generate_courier_data
from urls import Urls


@allure.feature('Авторизация курьера')
class TestLoginCourier:

    @allure.title('Курьер может успешно авторизоваться')
    def test_login_courier_success(self, registered_courier):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        }

        with allure.step('Отправить запрос на авторизацию'):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
                json=login_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код ответа и наличие id'):
            assert response.status_code == 200
            assert isinstance(response.json().get('id'), int)

    @allure.title(
        'Нельзя авторизоваться без обязательного поля: {missing_field}'
    )
    @pytest.mark.parametrize(
        'missing_field',
        ['login', 'password'],
        ids=['without_login', 'without_password'],
    )
    def test_login_without_required_field_returns_error(
        self,
        registered_courier,
        missing_field,
    ):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        }
        login_data[missing_field] = ''

        with allure.step(
            f'Отправить запрос с пустым полем {missing_field}'
        ):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
                json=login_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и сообщение об ошибке'):
            assert response.status_code == 400
            assert (
                ResponseMessages.LOGIN_MISSING_DATA
                in response.json()['message']
            )

    @allure.title(
        'Нельзя авторизоваться с неверным полем: {incorrect_field}'
    )
    @pytest.mark.parametrize(
        'incorrect_field',
        ['login', 'password'],
        ids=['incorrect_login', 'incorrect_password'],
    )
    def test_login_with_incorrect_credentials_returns_error(
        self,
        registered_courier,
        incorrect_field,
    ):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        }
        login_data[incorrect_field] += 'wrong'

        with allure.step(
            f'Отправить запрос с неверным полем {incorrect_field}'
        ):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
                json=login_data,
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и сообщение об ошибке'):
            assert response.status_code == 404
            assert (
                ResponseMessages.COURIER_NOT_FOUND
                in response.json()['message']
            )

    @allure.title(
        'Несуществующий курьер не может авторизоваться'
    )
    def test_login_nonexistent_courier_returns_error(self):
        courier_data = generate_courier_data()

        with allure.step(
            'Отправить данные незарегистрированного курьера'
        ):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
                json={
                    'login': courier_data['login'],
                    'password': courier_data['password'],
                },
                timeout=REQUEST_TIMEOUT,
            )

        with allure.step('Проверить код и сообщение об ошибке'):
            assert response.status_code == 404
            assert (
                'Учетная запись не найдена'
                in response.json()['message']
            )
