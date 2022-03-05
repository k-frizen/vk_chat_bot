# -*- coding: utf-8 -*-
import calendar
import datetime
from collections import defaultdict

from settings import CITIES, DATE_FORMAT


def routes_developer(cities: tuple[str, ...]) -> dict[str: list[str]]:
    """Создаёт маршруты из кортежа переданных городов

    :param cities: города для генерации маршрутов"""
    routes = defaultdict(list)
    cities_without_connection = {'Stockholm', 'Torshavn'}
    for departure_city in cities:
        for arrival_city in cities:
            if departure_city != arrival_city and {departure_city, arrival_city} != cities_without_connection:
                routes[departure_city].append(arrival_city)

    return routes


def create_schedule(departure_city: str, arrival_city: str, date: datetime.date) -> dict:
    """ Создаёт расписание: формирует словарь с номером рейса, 5 возможными датами и
     временем вылета, относительно данного дня.

    :param departure_city: город вылета
    :param arrival_city: город прибытия
    :param date: день, относительно которого генерируется расписание
    """
    every_ten_days_cities = {'Reykjavik', 'Torshavn'}  # two cities with flights at days even 10
    every_friday_days_cities = {'Stockholm', 'Reykjavik'}  # two cities with flights at fridays
    route = {departure_city, arrival_city}
    flight_number = f'SD{len(departure_city)}{len(arrival_city)}'  # 'Oslo', 'Stockholm' -> 'SD49'
    schedule = dict(flight_number=flight_number, time=['12:00'], dates=[])
    dates_list = schedule['dates']

    while len(dates_list) != 5:
        date += datetime.timedelta(days=1)
        day = datetime.date.strftime(date, DATE_FORMAT)
        if route == every_ten_days_cities:
            if not date.day % 10 or (date.day, date.month) == (1, 3):
                dates_list.append(day)
        elif route == every_friday_days_cities:
            if date.weekday() == 4:
                dates_list.append(day)
        else:
            dates_list.append(day)

    return schedule


ROUTES = routes_developer(CITIES)
