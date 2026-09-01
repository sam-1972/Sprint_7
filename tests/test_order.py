import allure
import pytest
import requests

from config import REQUEST_TIMEOUT
from data import ORDER_COLOR_CASES, build_order_data
from endpoints import Endpoints
from urls import Urls


@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Заказ создаётся с набором цветов: {colors}')
    @pytest.mark.parametrize(
        'colors',
        ORDER_COLOR_CASES,
        ids=['black', 'grey', 'black_and_grey', 'without_color'],
    )
    def test_create_order_with_different_colors_success(
        self,
        colors,
        created_order_tracks,
    ):
        order_data = build_order_data(colors)

        with allure.step('Отправить запрос на создание заказа'):
            response = requests.post(
                f'{Urls.BASE_URL}{Endpoints.CREATE_ORDER}',
                json=order_data,
                timeout=REQUEST_TIMEOUT,
            )

            response_body = response.json()
            track = response_body.get('track')

            with allure.step('Проверить код ответа и наличие track'):
                assert response.status_code == 201
                assert isinstance(track, int)

            created_order_tracks.append(track)
