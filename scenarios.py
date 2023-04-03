from config import USER_DATE_FORMAT
from constants import *
from wordings import *

SCENARIOS = {
    'Greeting': {
        FIRST_STEP: 'step1',
        STEPS: {
            'step1': {
                TEXT: WELCOME_MESSAGE,
                FAILURE_TEXT: CAN_HANDLE_TEXT_ONLY,
                HANDLER: 'greeting',
                NEXT_STEP: None,
            },
        }
    },
    'Help': {
        FIRST_STEP: 'step1',
        STEPS: {
            'step1': {
                TEXT: HELP_MESSAGE,
                FAILURE_TEXT: SELECT_ONE_COMMAND,
                HANDLER: 'help_handler',
                NEXT_STEP: None,
            },
        }
    },
    'Ordering': {
        FIRST_STEP: 'step1',
        STEPS: {
            'step1': {
                TEXT: ENTER_DEPARTURE_CITY,
                FAILURE_TEXT: SEND_TICKET,
                HANDLER: 'departure',
                NEXT_STEP: 'step2'
            },
            'step2': {
                TEXT: SEND_DEPARTURE_CITY,
                FAILURE_TEXT: CITY_MUST_BE_IN_LIST,
                HANDLER: 'routes',
                NEXT_STEP: 'step3'
            },
            'step3': {
                TEXT: FLIGHT_CHOSEN_BETWEEN + USER_DATE_FORMAT,
                FAILURE_TEXT: NO_FLIGHT_BETWEEN,
                HANDLER: 'route_info',
                NEXT_STEP: 'step4'
            },
            'step4': {
                TEXT: ENTER_DEPARTURE_DAY,
                FAILURE_TEXT: INCORRECT_DATE_FORMAT,
                HANDLER: 'date_handler',
                NEXT_STEP: 'step5'
            },
            'step5': {
                TEXT: SELECT_DEP_TIME,
                FAILURE_TEXT: TRY_AGAIN,
                HANDLER: 'departure_date_handler',
                NEXT_STEP: 'step5.1'
            },
            'step5.1': {
                TEXT: '',
                FAILURE_TEXT: TRY_AGAIN,
                HANDLER: 'departure_time_handler',
                NEXT_STEP: 'step6'
            },
            'step6': {
                TEXT: LEAVE_COMMENT,
                FAILURE_TEXT: 'От 1 до 5 включительно!',
                HANDLER: 'count_handler',
                NEXT_STEP: 'step7'
            },
            'step7': {
                TEXT: 'Данные верны?',
                FAILURE_TEXT: None,
                HANDLER: 'comment',
                NEXT_STEP: 'step8'
            },
            'step8': {
                TEXT: ENTER_PHONE_NUMBER,
                FAILURE_TEXT: RESTART_TO_CHANGE_DATA,
                HANDLER: 'data_correct',
                NEXT_STEP: 'step9'
            },
            'step9': {
                TEXT: YOUR_NAME,
                FAILURE_TEXT: TRY_AGAIN,
                HANDLER: 'phone_handler',
                NEXT_STEP: 'step10'
            },
            'step10': {
                TEXT: ORDER_INFO,
                FAILURE_TEXT: None,
                HANDLER: 'name_handler',
                IMAGE: 'generates_ticket_handler',
                NEXT_STEP: None
            }
        }
    }
}
