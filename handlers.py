import re
from datetime import datetime
from typing import Union

from vk_api.keyboard import VkKeyboard

from config import DATE_FORMAT
from constants import *
from generate_flights import router
from generate_ticket import TicketMaker
from keyboards import keyboards
from utils import get_commands_from_text, scenario_step_text, set_boarding_time, log


def greeting(text: str, context: dict) -> VkKeyboard:
    step_text = scenario_step_text('Greeting', 'step1')
    buttoms_text = get_commands_from_text(step_text)
    return keyboards.set_keyboard_buttons(buttoms_text)


def help_handler(text: str, context: dict) -> VkKeyboard:
    step_text = scenario_step_text(HELP_FLOW, 'step1')
    buttoms_text = get_commands_from_text(step_text)
    return keyboards.set_keyboard_buttons(buttoms_text)


def departure(text: str, context: dict) -> VkKeyboard:
    """ step 1 """
    return keyboards.set_keyboard_buttons(CITIES_LIST)


def routes(text: str, context: dict) -> bool or VkKeyboard:
    """ step 2 """
    city = text.title()
    if city in CITIES_LIST:
        context[DEPARTURE_CITY] = city

        buttons = router.routes[city]
        return keyboards.set_keyboard_buttons(buttons)
    else:
        return False


def route_info(text: str, context: dict) -> bool:
    """ step 3 """
    city = text.title()
    if city in CITIES_LIST:
        context[DESTINATION_CITY] = city
        return True
    else:
        return False


def date_handler(text: str, context: dict) -> Union[bool, VkKeyboard]:
    """ step 4 """
    try:
        date = datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        log.debug(f'incorrect date format! {text}.')
        return False

    if (date - date.today()).days < 0:
        return False

    schedule = router.schedule_creator(**context, date=date)
    context[FLIGHT_NUMBER] = schedule[FLIGHT_NUMBER]
    schedule.pop(FLIGHT_NUMBER)
    context[SCHEDULE] = schedule

    buttons = schedule[DATES]
    return keyboards.set_keyboard_buttons(buttons)


def departure_date_handler(text: str, context: dict) -> Union[bool, VkKeyboard]:
    """ step 5 """
    if text in context[SCHEDULE][DATES]:
        context[DEPARTURE_DATE] = text
        departure_time: list = context[SCHEDULE][TIME]
        return keyboards.set_keyboard_buttons(departure_time)
    else:
        return False


def departure_time_handler(text: str, context: dict):
    """ step 5.1 """
    if text in context[SCHEDULE][TIME]:
        context.pop(SCHEDULE)
        context[DEPARTURE_TIME] = text
        context[BOARDING_TIME] = set_boarding_time(context)

        buttons = tuple(range(1, 6))
        return keyboards.set_keyboard_buttons(buttons, one_line=True)
    else:
        return False


def count_handler(text: str, context: dict) -> Union[bool, VkKeyboard]:
    """ step 6 """
    try:
        count_of_tickets = int(text)
        assert 1 <= count_of_tickets <= 5
        context[COUNT_OF_TICKETS] = count_of_tickets
        context[TICKET] = 'билет' if text == '1' else 'билетов' if text == '5' else 'билета'

        buttons = ('Продолжить', RESTART_COMMAND)
        return keyboards.set_keyboard_buttons(buttons)

    except ValueError:
        log.debug(f'incorrect data: {text} can not be a integer!')
        return False
    except AssertionError:
        return False


def comment(text: str, context: dict) -> VkKeyboard:
    """ step 7 """
    context[COMMENT] = text if text != 'Продолжить' else ''
    buttons = ('Да', RESTART_COMMAND)
    return keyboards.set_keyboard_buttons(buttons)


def data_correct(text: str, context: dict) -> bool:
    """ step 8"""
    return True if text in ('Да', "да", 'Yes', 'yes', 'Y', 'y') else False


def phone_handler(text: str, context: dict) -> Union[bool, VkKeyboard]:
    """ step 9"""
    phone = re.match(r'\+?\d{1,3}[\d\-.\s()]{10,19}', text)
    if phone:
        context[PHONE] = text if text.startswith('+') else f'+{text}'
        buttons = ('Продолжить', RESTART_COMMAND)
        return keyboards.set_keyboard_buttons(buttons)
    else:
        log.info(f'Incorrect phone number {text}')
        return False


def name_handler(text: str, context: dict) -> bool:
    """ step 10"""
    if text != "Продолжить":
        context[NAME] = text
    return True


def generates_ticket_handler(text: str, context: dict) -> bytes:
    """ also step 10"""
    from random import randint, choice
    from string import ascii_uppercase

    context[SEAT] = '{row}{seat}'.format(
        row=randint(1, 32),
        seat=choice(ascii_uppercase[:5])  # from A to F
    )
    context[GATE] = '1'
    return TicketMaker().generate_ticket(context)
