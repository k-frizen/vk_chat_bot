import re
from datetime import datetime
from typing import Union

from vk_api.keyboard import VkKeyboard

from generate_flights import Router
from generate_ticket import TicketMaker
from keyboards import Keyboard
from settings import CITIES, DATE_FORMAT
from utils import get_commands_from_text, scenario_step_text, set_boarding_time, log


def greeting(text, context) -> VkKeyboard:
    step_text = scenario_step_text('Greeting', 'step1')
    buttoms_text = get_commands_from_text(step_text)
    return Keyboard().set_keyboard_buttons(buttoms_text)


def help_handler(text, context) -> VkKeyboard:
    step_text = scenario_step_text('Help', 'step1')
    buttoms_text = get_commands_from_text(step_text)
    return Keyboard().set_keyboard_buttons(buttoms_text)


def departure(text, context) -> VkKeyboard:
    """ step 1 """
    return Keyboard().set_keyboard_buttons(CITIES)


def routes(text, context) -> bool or VkKeyboard:
    """ step 2 """
    city = text.title()
    if city in CITIES:
        context['departure_city'] = city

        buttons = Router().routes[city]
        return Keyboard().set_keyboard_buttons(buttons)
    else:
        return False


def route_info(text, context) -> bool:
    """ step 3 """
    city = text.title()
    if city in CITIES:
        context['destination_city'] = city
        return True
    else:
        return False


def date_handler(text, context) -> Union[bool, VkKeyboard]:
    """ step 4 """
    try:
        date = datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        log.debug(f'incorrect date format! {text}.')
        return False

    if (date - date.today()).days < 0:
        return False

    schedule = Router().schedule_creator(
        departure_city=context['departure_city'],
        arrival_city=context['destination_city'],
        date=date
    )
    context['flight_number'] = schedule['flight_number']
    schedule.pop('flight_number')
    context['schedule'] = schedule

    buttons = schedule['dates']
    return Keyboard().set_keyboard_buttons(buttons)


def departure_date_handler(text, context) -> Union[bool, VkKeyboard]:
    """ step 5 """
    if text in context['schedule']['dates']:
        context['departure_date'] = text
        departure_time: list = context['schedule']['time']
        return Keyboard().set_keyboard_buttons(departure_time)
    else:
        return False


def departure_time_handler(text, context):
    """ step 5.1 """
    if text in context['schedule']['time']:
        context.pop('schedule')
        context['departure_time'] = text
        context['boarding_time'] = set_boarding_time(context)

        buttons = tuple(range(1, 6))
        return Keyboard().set_keyboard_buttons(buttons, one_line=True)
    else:
        return False


def count_handler(text, context) -> Union[bool, VkKeyboard]:
    """ step 6 """
    try:
        count_of_tickets = int(text)
        if 1 <= count_of_tickets <= 5:
            context['count_of_tickets'] = count_of_tickets
            context['ticket'] = 'билет' if text == '1' else 'билетов' if text == '5' else 'билета'

            buttons = ('Продолжить', '/restart')
            return Keyboard().set_keyboard_buttons(buttons)

        else:
            return False
    except ValueError:
        log.debug(f'incorrect data: {text} can not be a integer!')
        return False


def comment(text, context) -> VkKeyboard:
    """ step 7 """
    context['comment'] = text if text != 'Продолжить' else ''
    buttons = ('Да', '/restart')
    return Keyboard().set_keyboard_buttons(buttons)


def data_correct(text, context) -> bool:
    """ step 8"""
    return True if text in ('Да', "да", 'Yes', 'yes', 'Y', 'y') else False


def phone_handler(text, context) -> Union[bool, VkKeyboard]:
    """ step 9"""
    phone = re.match(r'\+?\d{1,3}[\d\-.\s()]{10,19}', text)
    if phone:
        context['phone'] = text if text.startswith('+') else f'+{text}'
        buttons = ('Продолжить', '/restart')
        return Keyboard().set_keyboard_buttons(buttons)
    else:
        log.info(f'Incorrect phone number {text}')
        return False


def name_handler(text, context) -> bool:
    """ step 10"""
    if text != "Продолжить":
        context['name'] = text
    return True


def generates_ticket_handler(text, context) -> bytes:
    """ also step 10"""
    from random import randint, choice
    from string import ascii_uppercase

    context['seat'] = '{row}{seat}'.format(
        row=randint(1, 32),
        seat=choice(ascii_uppercase[:5])  # from A to F
    )
    context['gate'] = '1'
    return TicketMaker().generate_ticket(context)
