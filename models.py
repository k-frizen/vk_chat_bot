from pony.orm import Database, Required, Json, Optional

from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """Содержит информацию о пользователе: id, шаг и название сценария,
    контекст с данными от пользователя"""
    user_id = Required(int, unique=True)
    step_name = Required(str)
    scenario_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """Данные, необходимые для регистрации пользователя на рейс"""
    name = Required(str)
    departure_city = Required(str)
    destination_city = Required(str)
    departure_date = Required(str)
    boarding_time = Required(str)
    departure_time = Required(str)
    flight_number = Required(str)
    seat = Required(str)
    gate = Required(str)
    count_of_tickets = Required(int)
    ticket = Required(str)
    phone = Required(str)
    comment = Optional(str)


db.generate_mapping(create_tables=True)
