# Sprint_7

Автоматизированные API-тесты обязательной части проекта для учебного
сервиса «Яндекс Самокат». Тесты написаны на Python с использованием
Requests, Pytest и Allure.

## Покрытые ручки

- `POST /api/v1/courier` — создание курьера;
- `POST /api/v1/courier/login` — авторизация курьера;
- `POST /api/v1/orders` — создание заказа;
- `GET /api/v1/orders` — получение списка заказов.

Тестовые курьеры создаются с уникальными данными и удаляются после тестов.
Созданные в тестах заказы отменяются после проверки.

## Структура проекта

- `tests/` — API-тесты, разделённые по ручкам;
- `conftest.py` — фикстуры создания и удаления тестовых данных;
- `config.py` — тайм-аут HTTP-запросов;
- `helpers.py` — генератор данных курьера;
- `data.py` — данные заказов и наборы параметризации;
- `endpoints.py` — пути API;
- `urls.py` — базовый адрес сервиса;
- `allure_results/` — результаты последнего запуска тестов.

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Запуск тестов

```bash
python3 -m pytest -v tests \
  --alluredir=allure_results \
  --clean-alluredir
```

## Просмотр Allure-отчёта

```bash
allure serve allure_results
```
