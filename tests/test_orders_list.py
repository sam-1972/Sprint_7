import allure
import requests

from config import REQUEST_TIMEOUT
from endpoints import Endpoints
from urls import Urls


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Ответ содержит список заказов')
    def test_get_orders_returns_orders_list(self):
        with allure.step('Отправить запрос на получение заказов'):
            response = requests.get(
                f'{Urls.BASE_URL}{Endpoints.GET_ORDERS}',
                timeout=REQUEST_TIMEOUT,
            )

        response_body = response.json()

        with allure.step('Проверить код и структуру ответа'):
            assert response.status_code == 200
            assert isinstance(response_body.get('orders'), list)
