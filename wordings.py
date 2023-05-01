from constants import CITIES_COMMAND, ROUTES_COMMAND, RESTART_COMMAND, TICKET_COMMAND, CITIES_LIST
from generate_flights import Router

DEFAULT_ANSWER = "Я могу помочь заказать билет. Введи /help для получения подробной информации или /ticket для заказа"

# GREETING
WELCOME_MESSAGE = """Добро пожаловать в scandinavian airlines bot, {name}!
Введи /ticket для заказа или /help для получения подробной информации"""
CAN_HANDLE_TEXT_ONLY = """Я могу обрабатывать только текстовые сообщения"""

# HELP
HELP_MESSAGE = f"""Если хочешь узнать все обслуживаемые города, отправь команду {CITIES_COMMAND}.
Выбери команду {ROUTES_COMMAND} чтобы узнать все возможные маршруты."""
SELECT_ONE_COMMAND = 'Выбери одну из команд!'

CITIES_COMMAND_TEXT = """{}\n\nЕсли хочешь заказать билет, отправь команду /ticket .
Введи команду /routes , чтобы узнать все обслуживаемые маршруты.""".format(
    '\n'.join(CITIES_LIST)
)
ROUTES_COMMAND_TEXT = '{}\n\nЕсли хочешь заказать билет, отправь команду /ticket.'.format(
    '\n'.join([' '.join([
        f'\nИз {departure}\nВ:', *arrival_list, '\n'
    ]) for departure, arrival_list in Router().routes.items()])
)

# ORDERING WORDINGS
ENTER_DEPARTURE_CITY = f"""Введи город отправления:\n\n
Ты можешь отправить команду {RESTART_COMMAND} для перезапуска заказа"""
SEND_TICKET = f'Введи {TICKET_COMMAND} для начала заказа'
SEND_DEPARTURE_CITY = 'Введи город прибытия:'
CITY_MUST_BE_IN_LIST = 'Город должен быть из списка: \n{}'.format('\n'.join(CITIES_LIST))
FLIGHT_CHOSEN_BETWEEN = """Был выбран рейс между {departure_city} и {destination_city}.
Введи день отправления в формате: """
NO_FLIGHT_BETWEEN = "Нет рейсов между этими городами"
ENTER_DEPARTURE_DAY = 'Выбери день вылета: '
INCORRECT_DATE_FORMAT = 'Некорректный формат или выбранный день уже прошёл! Попробуй снова'
SELECT_DEP_TIME = 'Был выбран день рейса {departure_date}. Выбери время вылета: '
ALL_FLIGHT_INFO = """Был выбран рейс между {departure_city} и {destination_city}\n
{departure_date}, в {departure_time}. Номер рейса: {flight_number}.
Введи количество билетов от 1 до 5"""
LEAVE_COMMENT = 'Твой заказ {count_of_tickets} {ticket}. Можешь оставить комментарий к заказу.'
ENTER_PHONE_NUMBER = 'Введи номер телефона в формате: +X XXXXXXXXXX'
YOUR_NAME = 'Укажи своё имя, если {name} не твоё настоящее имя'
ORDER_INFO = """Твой номер телефона {phone}.
Заказ: {count_of_tickets} {ticket} из {departure_city} в {destination_city} {departure_date} в {departure_time}."""

# ERROR MESSAGES
TRY_AGAIN = "Попробуй снова"
RESTART_TO_CHANGE_DATA = 'Отправь /restart чтобы изменить данные начав сначала'
CAN_NOT_HANDLE_THIS_TYPE = "Я не могу обрабатывать сообщения такого типа {}"
ONE_COMMAND_ONLY = 'Отправь только одну команду!'


if __name__ == '__main__':
    print(ROUTES_COMMAND_TEXT)