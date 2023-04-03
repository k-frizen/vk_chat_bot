from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from wordings import DEFAULT_ANSWER
from utils import get_commands_from_text


class Keyboard:

    def __init__(self):
        self.__keyboard = VkKeyboard(one_time=False, inline=False)

    def set_keyboard_buttons(self, buttons_text: tuple | list, one_line: bool = False) -> VkKeyboard:
        """Формирует клавиатуру с данными кнопками.

        :param buttons_text: надписи для кнопок клавиатуры
        :param one_line: должна ли быть клавиатура в одну линию. По умолчанию: False
        :rtype: VkKeyboard"""
        for i, unit in enumerate(buttons_text, start=1):
            self.__keyboard.add_button(label=unit, color=VkKeyboardColor.PRIMARY)
            if not i % 2 and i != len(buttons_text) and not one_line:
                self.__keyboard.add_line()

        if '/restart' not in buttons_text:
            self.__add_restart_button()
        return self.__keyboard

    def default_keyboard(self) -> str:
        """Возвращает клавиатуру с кнопками-командами из ответа по умолчанию

        :return: keyboard's json"""
        buttoms = get_commands_from_text(DEFAULT_ANSWER)
        keyboard = self.set_keyboard_buttons(buttoms)
        return keyboard.get_keyboard()

    def __add_restart_button(self) -> None:
        """"Добавляет в существующую клавиатуру кнопку с командой '/restart' """
        self.__keyboard.add_line()
        self.__keyboard.add_button(label='/restart', color=VkKeyboardColor.SECONDARY)

