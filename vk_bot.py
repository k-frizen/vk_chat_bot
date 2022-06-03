# -*- coding: utf-8 -*-
import random

import requests
from pony.orm import db_session
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard

import handlers
from utils import default_keyboard, get_commands_from_text, set_keyboard_buttons, compare_answer_to_user
from utils import user_state_exists, log, configure_logging
from models import UserState, Registration
from settings import SCENARIOS, INTENTS, DEFAULT_ANSWER, GROUP_ID, VK_BOT_TOKEN


class Bot:
    """Класс обеспечивает работу чат-бота для vk.com"""

    def __init__(self, group_id: int, token: str):
        self.group_id = group_id
        self.token = token

        self.vk = VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self) -> None:
        """Запуск бота"""
        for event in self.long_poller.listen():
            try:
                self.event_handler(event)
            except Exception as exc:
                log.exception(f'{exc} with event')

    @db_session
    def event_handler(self, event) -> None:
        """Метод обрабатывает event:
        получает состояние пользователя в сценарии,
        реагирует на полученную команду или
        ищет в тексте ключевое слово-намерение (intent).

        :param event: сообщение-событие, полученное от пользователя"""
        message = event.object.message
        user_id, text = message['peer_id'], message['text']
        user_name = self._get_name(user_id)

        if event.type == VkBotEventType.MESSAGE_NEW:
            state = UserState.get(user_id=user_id)
            commands = get_commands_from_text(text)

            if commands:
                self.commands_handler(commands=commands, user_id=user_id, user_name=user_name)
            elif state is not None:
                self.continue_scenario(text, state, user_id)
            else:
                self.intent_searching(text, user_name, user_id)

        else:
            self.send_message(f'Я не могу обрабатывать сообщения такого типа {event.type}', user_id)
            log.info('Unknown type: ', event.type)

    def intent_searching(self, text: str, user_name: str, user_id: int) -> None:
        """Ищет ключевое слово-намерение (intent) в тексте сообщения.

        :param text: текст сообщения
        :param user_name: полное имя пользователя
        :param user_id: user id (peer id)
        """
        for intent in INTENTS:
            if any(token in text.lower() for token in intent['tokens']):

                if intent['answer']:
                    reply_text = intent['answer'].format(user_name=user_name)
                    self.send_message(reply_text, user_id)
                else:
                    self.start_scenario(user_id, intent['scenario'], user_name, text=text)
                break

        else:
            self.send_message(DEFAULT_ANSWER, user_id, keyboard=default_keyboard())

    def send_message(self, answer: str, user_id: int, *, image: bytes = None, keyboard: str = '') -> None:
        """Обеспечивает отправку сообщения пользователю

        :param answer: текст сообщения
        :param user_id: user id
        :param image: изображение
        :param keyboard: json клавиатуры
        """
        attachment = self._get_image_data(image) if image else None
        self.api.messages.send(
            message=answer,
            random_id=random.randint(0, 2 ** 10),
            peer_id=user_id,
            attachment=attachment,
            keyboard=keyboard
        )

    def _get_image_data(self, image: bytes) -> str:
        """Получает необходимые данные с сервера vk.com для отправки изображения.

        :param image: изображение"""
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**data)[0]
        owner_id, image_id = image_data['owner_id'], image_data['id']
        return f'photo{owner_id}_{image_id}'

    @db_session
    def start_scenario(self, user_id: int, scenario_name: str, user_name: str, text: str) -> None:
        """Начинает сценарий, создаёт поле пользователя в базе данных UserState.
        Отправляет первое сообщение сценария.

        :param user_id: user id
        :param scenario_name: начинаемый сценарий
        :param user_name: имя пользователя
        :param text: текст сообщения"""
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        context = {'name': user_name}
        answer = step['text'].format(**context)
        keyboard = VkKeyboard.get_empty_keyboard()

        user_state_exists(user_id)
        if step['handler']:
            handler = getattr(handlers, step['handler'])
            reply = handler(text=text, context=context)

            if reply:
                if isinstance(reply, VkKeyboard):
                    keyboard = reply.get_keyboard()
            else:
                answer = DEFAULT_ANSWER
                keyboard = default_keyboard()

        self.send_message(answer, user_id, keyboard=keyboard)

        if step['next_step']:
            UserState(user_id=user_id, step_name=step['next_step'],
                      scenario_name=scenario_name, context=context)

    @db_session
    def continue_scenario(self, text, state, user_id) -> None:
        """Обеспечивает продолжение сценария, формирует ответ и клавиатуру.


        :param text: текст сообщения
        :param state: поле базы данных UserState -- "состояние" пользователя в сценарии (шаг)
        :param user_id: id пользователя"""
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        reply = handler(text=text, context=state.context)
        if reply:
            answer, image = step['text'], None
            keyboard = VkKeyboard.get_empty_keyboard()

            if isinstance(reply, str):
                answer = f"{answer}\n{reply}"

            elif isinstance(reply, VkKeyboard):
                keyboard = reply.get_keyboard()

            if 'image' in step:
                handler = getattr(handlers, step['image'])
                image = handler(text=text, context=state.context)

            self.send_message(
                answer.format(**state.context), user_id, image=image, keyboard=keyboard
            )

            if step['next_step']:  # next step exists?
                state.step_name = step['next_step']

            else:  # finish scenario
                log.info('New order')
                Registration(**state.context)
                state.delete()

        else:
            self.send_message(step['failure_text'], user_id)

    def _get_name(self, user_id: int) -> str:
        """Получает данные с сервера о имени пользователя.

        :param user_id: user id (peer id)
        :returns: полное имя пользователя: имя и фамилия"""
        data = self.vk.method("users.get", {"user_ids": user_id})[0]
        return "{} {}".format(data["first_name"], data["last_name"])

    def commands_handler(self, commands: tuple, user_id: int, user_name: str):
        """Обрабатывает команду, отправленную пользователем,
        и отправляет соответствующее ей сообщение и/или клавиатуру

        :param commands: текст команд(ы)
        :param user_name: имя пользователя
        :param user_id: id пользователя (peer id)
        """
        if len(commands) == 1:
            command = commands[0]
            match command:

                case '/help' | '/ticket':
                    scenario_name = 'Help' if command == '/help' else 'Ordering'
                    self.start_scenario(user_id, scenario_name, user_name, text=command)

                case '/cities' | '/routes':
                    text_to_send = compare_answer_to_user(command)
                    keyboard = set_keyboard_buttons(get_commands_from_text(text_to_send))
                    self.send_message(text_to_send, user_id, keyboard=keyboard.get_keyboard())

                case '/restart':
                    keyboard = default_keyboard()
                    self.send_message(DEFAULT_ANSWER, user_id, keyboard=keyboard)
                    user_state_exists(user_id)

        else:
            keyboard = set_keyboard_buttons(commands)
            self.send_message(
                answer='Отправь только одну команду!', user_id=user_id, keyboard=keyboard.get_keyboard()
            )


if __name__ == "__main__":
    bot = Bot(
        group_id=GROUP_ID,
        token=VK_BOT_TOKEN
    )
    bot.run()
    configure_logging()
