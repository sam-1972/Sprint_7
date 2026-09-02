import allure
import pytest

from api_methods import CourierApi
from data import ResponseMessages


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно успешно создать')
    def test_create_courier_success(self, courier_data):
        response = CourierApi.create_courier(courier_data)

        with allure.step('Проверить код и тело ответа'):
            assert response.status_code == 201
            assert response.json() == {'ok': True}

    @allure.title(
        'Нельзя создать двух одинаковых курьеров'
    )
    def test_create_duplicate_courier_returns_error(
        self,
        registered_courier,
    ):
        response = CourierApi.create_courier(registered_courier)

        with allure.step(
            'Проверить код и сообщение об ошибке'
        ):
            assert response.status_code == 409
            assert (
                ResponseMessages.DUPLICATE_COURIER
                in response.json()['message']
            )

    @allure.title(
        'Нельзя создать курьера без обязательного поля: '
        '{missing_field}'
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

        response = CourierApi.create_courier(incomplete_data)

        with allure.step(
            'Проверить код и сообщение об ошибке'
        ):
            assert response.status_code == 400
            assert (
                ResponseMessages.CREATE_COURIER_MISSING_DATA
                in response.json()['message']
            )
