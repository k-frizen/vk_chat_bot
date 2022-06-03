import logging
from datetime import datetime, timedelta
from typing import Union

from vk_api.keyboard import VkKeyboardColor, VkKeyboard

from generate_flights import ROUTES
from models import UserState
from settings import CITIES, DEFAULT_ANSWER, SCENARIOS, DATE_TIME_FORMAT, TIME_FORMAT, commands

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


def compare_answer_to_user(command: str) -> str:
    """Возвращает текст ответа для команды

    :param command: одна из команд бота (только '/cities' или '/routes')"""
    match command:

        case '/cities':
            return ('{}\n\nЕсли хочешь заказать билет, отправь команду /ticket .'
                    'Введи команду /routes , чтобы узнать все обслуживаемые маршруты.').format(
                '\n'.join(CITIES))

        case '/routes':
            answer = ''
            for departure, arrival_list in ROUTES.items():
                answer += ' '.join([
                    f'\nИз {departure}\n'
                    'В:', *arrival_list, '\n'
                ])
            return f'{answer}\n\n Если хочешь заказать билет, отправь команду /ticket .'


def set_keyboard_buttons(buttons_text: Union[tuple, list], one_line: bool = False) -> VkKeyboard:
    """Формирует клавиатуру с данными кнопками.

    :param buttons_text: надписи для кнопок клавиатуры
    :param one_line: должна ли быть клавиатура в одну линию. По умолчанию: False
    :rtype: VkKeyboard"""
    keyboard = VkKeyboard(one_time=False, inline=False)
    for i, unit in enumerate(buttons_text, start=1):
        keyboard.add_button(label=unit, color=VkKeyboardColor.PRIMARY)
        if not i % 2 and i != len(buttons_text) and not one_line:
            keyboard.add_line()

    if '/restart' not in buttons_text:
        keyboard.add_line()
        keyboard.add_button(label='/restart', color=VkKeyboardColor.SECONDARY)
    return keyboard


def get_commands_from_text(text: str) -> tuple:
    """Ищет команды в тексте

    :param text: текст, в котором будет производиться поиск
    :return: кортеж с командами из текста"""
    return tuple(word for word in text.split() if word in commands)


def default_keyboard() -> str:
    """Возвращает клавиатуру с кнопками-командами из ответа по умолчанию

    :return: keyboard's json"""
    buttoms = get_commands_from_text(DEFAULT_ANSWER)
    keyboard = set_keyboard_buttons(buttoms)
    return keyboard.get_keyboard()


def scenario_step_text(scenario_name: str, step_name: str) -> str:
    """Возвращает текст определённого шага сценария

    :param scenario_name: название сценария, текст шага которого нужно получить
    :param step_name: номер шага ('step_N') """
    return SCENARIOS[scenario_name]['steps'][step_name]['text']


def set_boarding_time(context: dict) -> str:
    """Вычисляет время окончания посадки: 30 минут до вылета

    :param context: информация о заказе
    :return: строка, содержащая время в формате hh:mm"""
    departure_datetime = f"{context['departure_date']} {context['departure_time']}"
    boarding_datetime = datetime.strptime(departure_datetime, DATE_TIME_FORMAT) - timedelta(minutes=30)
    return boarding_datetime.time().strftime(TIME_FORMAT)


def user_state_exists(user_id: int) -> None:
    """Удаляет "состояние" пользователя из базы данных UserState и сценария
    в случае перезапуска сценария или бота.

    :param user_id: id пользователя"""
    state = UserState.get(user_id=user_id)
    if state is not None:
        state.delete()
