import allure

from api_methods import OrderApi


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Ответ содержит список заказов')
    def test_get_orders_returns_orders_list(self):
        response = OrderApi.get_orders()
        response_body = response.json()

        with allure.step(
            'Проверить код и структуру ответа'
        ):
            assert response.status_code == 200
            assert isinstance(response_body.get('orders'), list)
