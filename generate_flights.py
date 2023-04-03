# -*- coding: utf-8 -*-
import datetime
from collections import defaultdict

from config import DATE_FORMAT
from constants import CITIES_LIST, CITIES_WITHOUT_CONNECTION, EVERY_TEN_DAYS_CITIES, EVERY_FRIDAY_CITIES


class Router:
    def __init__(self, cities: tuple = CITIES_LIST, days_in_schedule: int = 5):
        self.cities = cities
        self.routes = self.routes_creator()
        self.count_of_days_in_schedule = days_in_schedule

    def routes_creator(self):
        """Создаёт маршруты из кортежа городов, переданных в параметр cities"""
        routes = defaultdict(list)
        for departure_city in self.cities:
            for arrival_city in self.cities:
                if departure_city != arrival_city and {departure_city, arrival_city} != CITIES_WITHOUT_CONNECTION:
                    routes[departure_city].append(arrival_city)
        return routes

    def schedule_creator(self, departure_city: str, destination_city: str, date: datetime.date, **kwargs) -> dict:
        """ Создаёт расписание: формирует словарь с номером рейса, возможными датами и временем вылета,
        относительно данного дня. Количество дней в расписании задаётся с помощью
        атрибута класса days_in_schedule (по умолчанию равен 5).

        :param departure_city: город вылета
        :param destination_city: город прибытия
        :param date: день, относительно которого генерируется расписание
        """
        route = {departure_city, destination_city}
        flight_number = f'SD{len(departure_city)}{len(destination_city)}'  # 'Oslo', 'Stockholm' -> 'SD49'
        schedule = dict(flight_number=flight_number, time=['12:00'], dates=[])
        dates_list = schedule['dates']

        while len(dates_list) != self.count_of_days_in_schedule:
            date += datetime.timedelta(days=1)
            day = datetime.date.strftime(date, DATE_FORMAT)
            if route == EVERY_TEN_DAYS_CITIES:
                if not date.day % 10 or (date.day, date.month) == (1, 3):
                    dates_list.append(day)
            elif route == EVERY_FRIDAY_CITIES:
                if date.weekday() == 4:
                    dates_list.append(day)
            else:
                dates_list.append(day)

        return schedule
