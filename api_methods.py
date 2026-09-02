import allure
import requests

from config import REQUEST_TIMEOUT
from endpoints import Endpoints
from urls import Urls


class CourierApi:

    @staticmethod
    @allure.step('Создать курьера')
    def create_courier(courier_data):
        return requests.post(
            f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}',
            json=courier_data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step('Авторизовать курьера')
    def login_courier(login_data):
        return requests.post(
            f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}',
            json=login_data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step('Удалить курьера с id {courier_id}')
    def delete_courier(courier_id):
        return requests.delete(
            f'{Urls.BASE_URL}{Endpoints.DELETE_COURIER}{courier_id}',
            timeout=REQUEST_TIMEOUT,
        )


class OrderApi:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data):
        return requests.post(
            f'{Urls.BASE_URL}{Endpoints.CREATE_ORDER}',
            json=order_data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step('Получить список заказов')
    def get_orders():
        return requests.get(
            f'{Urls.BASE_URL}{Endpoints.GET_ORDERS}',
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step('Отменить заказ с треком {track}')
    def cancel_order(track):
        return requests.put(
            f'{Urls.BASE_URL}{Endpoints.CANCEL_ORDER}',
            params={'track': track},
            timeout=REQUEST_TIMEOUT,
        )
