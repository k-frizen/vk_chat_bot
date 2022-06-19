# -*- coding: utf-8 -*-
import os
import unittest
from copy import deepcopy
from unittest.mock import Mock, patch

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent

from dataset import INPUTS, RAW_EVENT, EXCEPTED_OUTPUTS, context
from generate_ticket import TicketMaker
from settings import TEST_TICKET_PATH
from vk_bot import Bot


def isolate_db(func):
    def wrapper(*args, **kwargs):
        with db_session:
            func(*args, **kwargs)
            rollback()

    return wrapper


class TestBot(unittest.TestCase):

    @isolate_db
    def test_run(self):
        obj, count = {'a': 1}, 5
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('vk_bot.VkApi'):
            with patch('vk_bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot(0, '')
                bot.event_handler = Mock()
                bot.__get_image_data = Mock(return_value='photo12_34')
                bot._get_name = Mock(return_value=context['name'])
                bot.run()

                bot.event_handler.assert_called()
                bot.event_handler.assert_any_call(obj)
                self.assertEqual(bot.event_handler.call_count, count)

    @isolate_db
    def test_text_handler(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in INPUTS:
            event = deepcopy(RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)
        with patch('vk_bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot(0, '')
            bot.api = api_mock
            bot._get_image_data = Mock()
            bot._get_name = Mock(return_value=context['name'])
            bot.run()

        self.assertEqual(send_mock.call_count, len(INPUTS))

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

        self.assertEqual(real_outputs, EXCEPTED_OUTPUTS)

    def test_ticket(self):
        TicketMaker().create_test_boarding_pass(TEST_TICKET_PATH, context)
        ticket_bytes = TicketMaker().generate_ticket(context)
        with open(TEST_TICKET_PATH, 'rb') as ticket_example:
            content = ticket_example.read()

        self.assertEqual(ticket_bytes, content)
        os.remove(TEST_TICKET_PATH)


if __name__ == "__main__":
    unittest.main()
