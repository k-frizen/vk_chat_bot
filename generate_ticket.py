from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from config import TICKET_TEMPLATE_PATH, FONT_PATH, FONT_SIZE_CITIES, FONT_SIZE


class TicketMaker:
    """Класс, отвечающий за генерацию изображения посадочного талона (билета) пассажира"""

    def __init__(self, template_path: str = TICKET_TEMPLATE_PATH):
        self.base = Image.open(template_path).convert('RGBA')
        self.draw = ImageDraw.Draw(self.base)

    def write_text(self, coord: tuple, text: str,
                   colour: tuple = (0, 0, 0, 255),  # black
                   font: FreeTypeFont = ImageFont.truetype(FONT_PATH, FONT_SIZE)) -> None:
        """Наносит текст на изображение

        :param coord: координаты точки для нанесения текста
        :param text: текстовые данные
        :param colour: цвет в формате RGBA
        :param font: шрифт, который будет использоваться для нанесения информации
        """
        self.draw.text(coord, text, font=font, fill=colour)

    def generate_ticket(self, ticket_data: dict) -> bytes:
        """Создаёт посадочный талон, нанося на шаблон информацию о рейсе.

        :param ticket_data: источник данных о полёте
        :return: билет со всей информацией о пассажире и полёте
        """
        x1, y1 = 315, 810
        y2 = 1050
        x3 = 1666
        cities_font = ImageFont.truetype(FONT_PATH, FONT_SIZE_CITIES)

        self.write_text((x1, 400), ticket_data['departure_city'], font=cities_font)
        self.write_text((x1, 520), ticket_data['destination_city'], font=cities_font)
        self.write_text((x1, y1), ticket_data['name'])

        self.write_text((x1, y2), ticket_data['departure_date'])
        self.write_text((640, y2), ticket_data['departure_time'])
        self.write_text((954, y2), ticket_data['boarding_time'])
        self.write_text((x3, y2), ticket_data['gate'])

        self.write_text((x3, y1), ticket_data['seat'])
        self.write_text((x3, 570), ticket_data['flight_number'])

        return self.create_ticket_bytes()

    def create_ticket_bytes(self) -> bytes:
        """Возвращает билет в байтовом представлении"""
        self.base.seek(0)
        roiImg = self.base.crop()
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
