# -*- coding: utf-8 -*-

from constants import *
from utils import set_answer_to_user, scenario_step_text, set_dates
from wordings import DEFAULT_ANSWER

RAW_EVENT = {
    'type': 'message_new',
    'object': {
        'message': {
            'date': 1637772220, 'from_id': 48055049, 'id': 315, 'out': 0, 'peer_id': 48055049,
            'text': '', 'attachments': [], 'conversation_message_id': 313, 'fwd_messages': [],
            'important': False, 'is_hidden': False, 'random_id': 0
        },
        'client_info': {
            'button_actions': [
                'text', 'vkpay', 'open_app', 'location', 'open_link',
                'callback', 'intent_subscribe', 'intent_unsubscribe'
            ],
            'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 3}},
    'group_id': 208934186, 'event_id': '573e30df7cf055a9856afcb167e3434163b3fa89'}

inputted_date, departure_date = set_dates()

context = {
    COMMENT: COMMENT,
    COUNT_OF_TICKETS: 1,
    DEPARTURE_CITY: OSLO,
    DEPARTURE_DATE: departure_date,
    DEPARTURE_TIME: '12:00',
    BOARDING_TIME: '11:30',
    DESTINATION_CITY: STOCKHOLM,
    FLIGHT_NUMBER: 'SD49',
    NAME: 'Jack Shephard',
    PHONE: '+1481 5162342',
    TICKET: 'билет',
    SEAT: '23A',
    GATE: '1'
}

INPUTS = [
    'Hi!',  # 0
    HELP_COMMAND,  # 1
    CITIES_COMMAND,  # 2
    ROUTES_COMMAND,  # 3
    RESTART_COMMAND,  # 4
    TICKET_COMMAND,  # 5
    context[DEPARTURE_CITY],  # 6
    context[DESTINATION_CITY],  # 7
    inputted_date,  # 8
    departure_date,  # 9
    context[DEPARTURE_TIME],  # 10
    str(context[COUNT_OF_TICKETS]),  # 11
    'Продолжить',  # 12
    'Да',  # 13
    context[PHONE],  # 14
    'Продолжить',  # 15
]

EXCEPTED_OUTPUTS = [
    scenario_step_text('Greeting', 'step1').format(**context),  # 0
    scenario_step_text(HELP_FLOW, 'step1'),  # 1
    set_answer_to_user(INPUTS[2]),  # 2
    set_answer_to_user(INPUTS[3]),  # 3
    DEFAULT_ANSWER,  # 4
    scenario_step_text(ORDERING_FLOW, 'step1').format(**context),  # 5
    scenario_step_text(ORDERING_FLOW, 'step2').format(**context),  # 6
    scenario_step_text(ORDERING_FLOW, 'step3').format(**context),  # 7
    scenario_step_text(ORDERING_FLOW, 'step4').format(**context),  # 8
    scenario_step_text(ORDERING_FLOW, 'step5').format(**context),  # 9
    scenario_step_text(ORDERING_FLOW, 'step5.1').format(**context),  # 10
    scenario_step_text(ORDERING_FLOW, 'step6').format(**context),  # 11
    scenario_step_text(ORDERING_FLOW, 'step7').format(**context),  # 12
    scenario_step_text(ORDERING_FLOW, 'step8').format(**context),  # 13
    scenario_step_text(ORDERING_FLOW, 'step9').format(**context),  # 14
    scenario_step_text(ORDERING_FLOW, 'step10').format(**context),  # 15
]
