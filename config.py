import os
from dotenv import load_dotenv

load_dotenv('.env')

VK_BOT_TOKEN = os.getenv('VK_BOT_TOKEN')
GROUP_ID = int(os.getenv('GROUP_ID'))
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password=DB_PASSWORD,
    host='localhost',
    database='scandinavian_airlines_bot'
)

# Datetime format settings
DATE_FORMAT = '%d/%m/%Y'
USER_DATE_FORMAT = 'dd/mm/yyyy'
TIME_FORMAT = '%H:%M'
DATE_TIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# Ticket settings
TEST_TICKET_PATH = os.path.normpath('external_data/ticket/ticket_test.png')
TICKET_TEMPLATE_PATH = os.path.normpath('external_data/ticket/ticket_template.png')
FONT_PATH = os.path.normpath('external_data/fonts/Stolzl-Medium.ttf')
FONT_SIZE_CITIES = 78
FONT_SIZE = 51
