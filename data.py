from datetime import date, timedelta


ORDER_COLOR_CASES = [
    ['BLACK'],
    ['GREY'],
    ['BLACK', 'GREY'],
    None,
]

class ResponseMessages:
    DUPLICATE_COURIER = 'Этот логин уже используется'
    CREATE_COURIER_MISSING_DATA = (
        'Недостаточно данных для создания учетной записи'
    )
    LOGIN_MISSING_DATA = 'Недостаточно данных для входа'
    COURIER_NOT_FOUND = 'Учетная запись не найдена'

def build_order_data(colors):
    order_data = {
        'firstName': 'Виталий',
        'lastName': 'Бикеев',
        'address': 'Москва, улица Льва Толстого, дом 16',
        'metroStation': 1,
        'phone': '+79998887777',
        'rentTime': 4,
        'deliveryDate': (
            date.today() + timedelta(days=1)
        ).isoformat(),
        'comment': 'Позвоните перед доставкой',
    }

    if colors is not None:
        order_data['color'] = colors

    return order_data
