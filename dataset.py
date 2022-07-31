# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from settings import DEFAULT_ANSWER, DATE_FORMAT
from utils import set_answer_to_user, scenario_step_text


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


RAW_EVENT = {
    'type': 'message_new',
    'object': {
        'message': {
            'date': 1637772220, 'from_id': 48055049, 'id': 315, 'out': 0, 'peer_id': 48055049,
            'text': '', 'attachments': [], 'conversation_message_id': 313, 'fwd_messages': [],
            'important': False, 'is_hidden': False, 'random_id': 0},
        'client_info': {
            'button_actions': [
                'text', 'vkpay', 'open_app', 'location', 'open_link',
                'callback', 'intent_subscribe', 'intent_unsubscribe'
            ],
            'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 3}},
    'group_id': 208934186, 'event_id': '573e30df7cf055a9856afcb167e3434163b3fa89'}

inputted_date, departure_date = set_dates()

context = {
    'comment': 'comment',
    'count_of_tickets': 1,
    'departure_city': 'Oslo',
    'departure_date': departure_date,
    'departure_time': '12:00',
    'boarding_time': '11:30',
    'destination_city': 'Stockholm',
    'flight_number': 'SD49',
    'name': 'Jack Shephard',
    'phone': '+1481 5162342',
    'ticket': 'билет',
    'seat': '23A',
    'gate': '1'
}

INPUTS = [
    'Hi!',  # 0
    '/help',  # 1
    '/cities',  # 2
    '/routes',  # 3
    '/restart',  # 4
    '/ticket',  # 5
    context['departure_city'],  # 6
    context['destination_city'],  # 7
    inputted_date,  # 8
    departure_date,  # 9
    context['departure_time'],  # 10
    str(context['count_of_tickets']),  # 11
    'Продолжить',  # 12
    'Да',  # 13
    context['phone'],  # 14
    'Продолжить',  # 15
]

EXCEPTED_OUTPUTS = [
    scenario_step_text('Greeting', 'step1').format(**context),  # 0
    scenario_step_text('Help', 'step1'),  # 1
    set_answer_to_user(INPUTS[2]),  # 2
    set_answer_to_user(INPUTS[3]),  # 3
    DEFAULT_ANSWER,  # 4
    scenario_step_text('Ordering', 'step1').format(**context),  # 5
    scenario_step_text('Ordering', 'step2').format(**context),  # 6
    scenario_step_text('Ordering', 'step3').format(**context),  # 7
    scenario_step_text('Ordering', 'step4').format(**context),  # 8
    scenario_step_text('Ordering', 'step5').format(**context),  # 9
    scenario_step_text('Ordering', 'step5.1').format(**context),  # 10
    scenario_step_text('Ordering', 'step6').format(**context),  # 11
    scenario_step_text('Ordering', 'step7').format(**context),  # 12
    scenario_step_text('Ordering', 'step8').format(**context),  # 13
    scenario_step_text('Ordering', 'step9').format(**context),  # 14
    scenario_step_text('Ordering', 'step10').format(**context),  # 15
]
