from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from config import TICKET_TEMPLATE_PATH, FONT_PATH, FONT_SIZE_CITIES, FONT_SIZE
from constants import *


class TicketMaker:
    """Класс, отвечающий за генерацию изображения посадочного талона (билета) пассажира"""

    def __init__(self, template_path: str = TICKET_TEMPLATE_PATH):
        self.__base = Image.open(template_path).convert('RGBA')
        self.__draw = ImageDraw.Draw(self.__base)

    def _write_text(self, coord: tuple, text: str,
                    color: tuple = (0, 0, 0, 255),  # black
                    font: FreeTypeFont = ImageFont.truetype(FONT_PATH, FONT_SIZE)) -> None:
        """Наносит текст на изображение

        :param coord: координаты точки для нанесения текста
        :param text: текстовые данные
        :param color: цвет в формате RGBA
        :param font: шрифт, который будет использоваться для нанесения информации
        """
        self.__draw.text(coord, text, font=font, fill=color)

    def generate_ticket(self, ticket_data: dict) -> bytes:
        """Создаёт посадочный талон, нанося на шаблон информацию о рейсе.

        :param ticket_data: источник данных о полёте
        :return: билет со всей информацией о пассажире и полёте
        """
        x1, y1 = 315, 810
        y2 = 1050
        x3 = 1666
        cities_font = ImageFont.truetype(FONT_PATH, FONT_SIZE_CITIES)

        self._write_text((x1, 400), ticket_data[DEPARTURE_CITY], font=cities_font)
        self._write_text((x1, 520), ticket_data[DESTINATION_CITY], font=cities_font)
        self._write_text((x1, y1), ticket_data[NAME])

        self._write_text((x1, y2), ticket_data[DEPARTURE_DATE])
        self._write_text((640, y2), ticket_data[DEPARTURE_TIME])
        self._write_text((954, y2), ticket_data[BOARDING_TIME])
        self._write_text((x3, y2), ticket_data[GATE])

        self._write_text((x3, y1), ticket_data[SEAT])
        self._write_text((x3, 570), ticket_data[FLIGHT_NUMBER])

        return self._create_ticket_bytes()

    def _create_ticket_bytes(self) -> bytes:
        """Возвращает билет в байтовом представлении"""
        self.__base.seek(0)
        roiImg = self.__base.crop()
        imgByteArr = BytesIO()
        roiImg.save(imgByteArr, format='PNG')
        ticket_as_bytes = imgByteArr.getvalue()
        return ticket_as_bytes

    def create_test_boarding_pass(self, test_ticket_path: str, ticket_data: dict) -> None:
        """Создаёт тестовый билет

        :param test_ticket_path: путь до файла
        :param ticket_data: данные о рейсе"""
        with open(test_ticket_path, 'wb') as ticket:
            boarding_pass = self.generate_ticket(ticket_data)
            ticket.write(boarding_pass)
