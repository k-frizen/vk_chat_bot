import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

FONT_SIZE_CITIES, FONT_SIZE = 78, 51
COLOUR = (0, 0, 0, 255)  # black
template = os.path.normpath('external_data/ticket/ticket_template.png')
font_path = os.path.normpath('external_data/fonts/Stolzl-Medium.ttf')


def generate_ticket(ticket_data: dict) -> bytes:
    """Создаёт посадочный талон, нанося на шаблон информацию о рейсе.

    :param ticket_data: источник данных о полёте
    :return: билет со всей информацией о пассажире и полёте
    """
    base = Image.open(template).convert('RGBA')
    default_font = ImageFont.truetype(font_path, FONT_SIZE)
    cities_font = ImageFont.truetype(font_path, FONT_SIZE_CITIES)
    draw = ImageDraw.Draw(base)
    x1 = 315
    y1 = 810
    y2 = 1050
    x3 = 1666

    draw.text((x1, 400), ticket_data['departure_city'], font=cities_font, fill=COLOUR)
    draw.text((x1, 520), ticket_data['destination_city'], font=cities_font, fill=COLOUR)
    draw.text((x1, y1), ticket_data['name'], font=default_font, fill=COLOUR)

    draw.text((x1, y2), ticket_data['departure_date'], font=default_font, fill=COLOUR)
    draw.text((640, y2), ticket_data['departure_time'], font=default_font, fill=COLOUR)
    draw.text((954, y2), ticket_data['boarding_time'], font=default_font, fill=COLOUR)
    draw.text((x3, y2), ticket_data['gate'], font=default_font, fill=COLOUR)

    draw.text((x3, y1), ticket_data['seat'], font=default_font, fill=COLOUR)
    draw.text((x3, 570), ticket_data['flight_number'], font=default_font, fill=COLOUR)

    base.seek(0)
    roiImg = base.crop()
    imgByteArr = BytesIO()
    roiImg.save(imgByteArr, format='PNG')
    ticket_as_bytes = imgByteArr.getvalue()
    return ticket_as_bytes


def create_test_boarding_pass(test_ticket_path: str, ticket_data: dict) -> None:
    """Создаёт тестовый билет

    :param test_ticket_path: путь до файла
    :param ticket_data: данные о рейсе"""
    with open(test_ticket_path, 'wb') as ticket:
        boarding_pass = generate_ticket(ticket_data)
        ticket.write(boarding_pass)
