# CITIES
OSLO, COPENHAGEN, TORSHAVN = 'Oslo', 'Copenhagen', 'Torshavn'
REYKJAVIK, STOCKHOLM = 'Reykjavik', 'Stockholm'
CITIES_LIST = OSLO, COPENHAGEN, REYKJAVIK, TORSHAVN, STOCKHOLM

CITIES_WITHOUT_CONNECTION = STOCKHOLM, TORSHAVN
EVERY_TEN_DAYS_CITIES = REYKJAVIK, TORSHAVN  # two cities with flights at days even 10
EVERY_FRIDAY_CITIES = STOCKHOLM, REYKJAVIK  # two cities with flights at fridays

# SCENARIOS CONSTANTS
STEP, FIRST_STEP, NEXT_STEP = 'step', 'first_step', 'next_step'
STEPS, TEXT, FAILURE_TEXT = f'{STEP}s', 'text', 'failure_text'
HANDLER, IMAGE = 'handler', 'image'

# COMMANDS
TICKET_COMMAND, HELP_COMMAND, CITIES_COMMAND = '/ticket', '/help', '/cities'
ROUTES_COMMAND, RESTART_COMMAND = '/routes', '/restart'
COMMANDS = TICKET_COMMAND, HELP_COMMAND, CITIES_COMMAND, ROUTES_COMMAND, RESTART_COMMAND

# SCENARIOS NAMES
HELP_FLOW, ORDERING_FLOW = 'Help', 'Ordering'

# CONTEXT VARIABLES
DEPARTURE_CITY, DESTINATION_CITY = 'departure_city', 'destination_city'
FLIGHT_NUMBER, DATES = 'flight_number', 'dates'
SCHEDULE, TIME = 'schedule', 'time'
DEPARTURE_DATE, DEPARTURE_TIME = 'departure_date', 'departure_time'
BOARDING_TIME, TICKET = 'boarding_time', 'ticket'
COUNT_OF_TICKETS = 'count_of_tickets'
COMMENT, PHONE = 'comment', 'phone'
NAME, GATE, SEAT = 'name', 'gate', 'seat'

INTENTS = [
    {
        'name': 'Order ticket',
        'tokens': ('заказ', 'купить', 'найти', 'полёт'),
        'scenario': 'Ordering',
        'answer': None
    },
    {
        'name': 'Greeting',
        'tokens': ('hi', 'hello', 'здравствуй', 'прив'),
        'scenario': 'Greeting',
        'answer': None
    }
]
