import logging
from datetime import datetime, timedelta

from config import TIME_FORMAT, DATE_TIME_FORMAT, DATE_FORMAT
from constants import COMMANDS, TEXT, STEPS, DEPARTURE_DATE, DEPARTURE_TIME
from models import UserState
from scenarios import SCENARIOS
from wordings import CITIES_COMMAND_TEXT, ROUTES_COMMAND_TEXT

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
            return CITIES_COMMAND_TEXT

        case '/routes':
            return ROUTES_COMMAND_TEXT


def get_commands_from_text(text: str) -> tuple[str]:
    """Ищет команды в тексте

    :param text: текст, в котором будет производиться поиск
    :return: кортеж с командами из текста"""
    return tuple(filter(lambda word: word in COMMANDS, text.split()))


def scenario_step_text(scenario_name: str, step_name: str) -> str:
    """Возвращает текст определённого шага сценария

    :param scenario_name: название сценария, текст шага которого нужно получить
    :param step_name: номер шага ('step_N') """
    return SCENARIOS[scenario_name][STEPS][step_name][TEXT]


def set_boarding_time(context: dict) -> str:
    """Вычисляет время окончания посадки: 30 минут до вылета

    :param context: информация о заказе
    :return: строка, содержащая время в формате hh:mm"""
    departure_str_time = f"{context[DEPARTURE_DATE]} {context[DEPARTURE_TIME]}"
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


def set_dates() -> tuple[str, str]:
    """Возвращает две даты:
    1) дату-имитацию ввода пользователем желаемой даты вылета (через неделю относительно сегодняшнего дня)
    2) дату-имитацию выбора пользователем действительной даты вылета (на следующий день
    относительно желаемой даты вылета)"""
    date_for_test = datetime.today() + timedelta(days=7)
    input_date = date_for_test.strftime(DATE_FORMAT)

    user_choice_date = date_for_test + timedelta(days=1)
    real_departure_date = user_choice_date.strftime(DATE_FORMAT)
    return input_date, real_departure_date
