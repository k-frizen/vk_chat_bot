import logging
from datetime import datetime, timedelta

from generate_flights import Router
from models import UserState
from settings import CITIES, SCENARIOS, DATE_TIME_FORMAT, TIME_FORMAT, commands

log = logging.getLogger('bot')


def configure_logging() -> None:
    """Обеспечивает логирование"""
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("bot.log")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", DATE_TIME_FORMAT))
    file_handler.setLevel(logging.DEBUG)
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)


def set_answer_to_user(command: str) -> str:
    """Возвращает текст ответа для команды

    :param command: одна из команд бота (только '/cities' или '/routes')"""
    match command:

        case '/cities':
            return ('{}\n\nЕсли хочешь заказать билет, отправь команду /ticket .'
                    'Введи команду /routes , чтобы узнать все обслуживаемые маршруты.').format(
                '\n'.join(CITIES))

        case '/routes':
            answer = ''
            for departure, arrival_list in Router().routes.items():
                one_city_routes = [
                    f'\nИз {departure}\n'
                    'В:', *arrival_list, '\n'
                ]
                answer += ' '.join(one_city_routes)
            return f'{answer}\n\n Если хочешь заказать билет, отправь команду /ticket .'


def get_commands_from_text(text: str) -> tuple[str]:
    """Ищет команды в тексте

    :param text: текст, в котором будет производиться поиск
    :return: кортеж с командами из текста"""
    return tuple(filter(lambda word: word in commands, text.split()))


def scenario_step_text(scenario_name: str, step_name: str) -> str:
    """Возвращает текст определённого шага сценария

    :param scenario_name: название сценария, текст шага которого нужно получить
    :param step_name: номер шага ('step_N') """
    return SCENARIOS[scenario_name]['steps'][step_name]['text']


def set_boarding_time(context: dict) -> str:
    """Вычисляет время окончания посадки: 30 минут до вылета

    :param context: информация о заказе
    :return: строка, содержащая время в формате hh:mm"""
    departure_str_time = f"{context['departure_date']} {context['departure_time']}"
    departure_datetime = datetime.strptime(departure_str_time, DATE_TIME_FORMAT)
    boarding_datetime = departure_datetime - timedelta(minutes=30)
    return boarding_datetime.time().strftime(TIME_FORMAT)


def user_state_exists(user_id: int) -> None:
    """Удаляет "состояние" пользователя из базы данных UserState и сценария
    в случае перезапуска сценария или бота.

    :param user_id: id пользователя"""
    state = UserState.get(user_id=user_id)
    if state is not None:
        state.delete()
