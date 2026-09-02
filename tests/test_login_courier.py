import allure
import pytest

from api_methods import CourierApi
from data import ResponseMessages
from helpers import generate_courier_data


@allure.feature('Авторизация курьера')
class TestLoginCourier:

    @allure.title(
        'Курьер может успешно авторизоваться'
    )
    def test_login_courier_success(self, registered_courier):
        login_data = {
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        }
        response = CourierApi.login_courier(login_data)

        with allure.step(
            'Проверить код ответа и наличие id'
        ):
            assert response.status_code == 200
            assert isinstance(response.json().get('id'), int)

    @allure.title(
        'Нельзя авторизоваться без обязательного поля: '
        '{missing_field}'
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

        response = CourierApi.login_courier(login_data)

        with allure.step(
            'Проверить код и сообщение об ошибке'
        ):
            assert response.status_code == 400
            assert (
                ResponseMessages.LOGIN_MISSING_DATA
                in response.json()['message']
            )

    @allure.title(
        'Нельзя авторизоваться с неверным полем: '
        '{incorrect_field}'
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

        response = CourierApi.login_courier(login_data)

        with allure.step(
            'Проверить код и сообщение об ошибке'
        ):
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
        login_data = {
            'login': courier_data['login'],
            'password': courier_data['password'],
        }

        response = CourierApi.login_courier(login_data)

        with allure.step(
            'Проверить код и сообщение об ошибке'
        ):
            assert response.status_code == 404
            assert (
                ResponseMessages.COURIER_NOT_FOUND
                in response.json()['message']
            )
