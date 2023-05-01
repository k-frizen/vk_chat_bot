from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from utils import get_commands_from_text
from wordings import DEFAULT_ANSWER
from constants import RESTART_COMMAND


class _Keyboard:
    @staticmethod
    def __new_keyboard(*, one_time: bool = False, inline: bool = False) -> VkKeyboard:
        return VkKeyboard(one_time=one_time, inline=inline)

    def set_keyboard_buttons(self, buttons_text: tuple | list, one_line: bool = False) -> VkKeyboard:
        """Формирует клавиатуру с данными кнопками.

        :param buttons_text: надписи для кнопок клавиатуры
        :param one_line: должна ли быть клавиатура в одну линию. По умолчанию: False
        :rtype: VkKeyboard"""
        keyboard = self.__new_keyboard()
        for i, unit in enumerate(buttons_text, start=1):
            keyboard.add_button(label=unit, color=VkKeyboardColor.PRIMARY)
            if not i % 2 and i != len(buttons_text) and not one_line:
                keyboard.add_line()

        if RESTART_COMMAND not in buttons_text:
            self.__add_restart_button(keyboard)
        return keyboard

    def default_keyboard(self) -> str:
        """Возвращает клавиатуру с кнопками-командами из ответа по умолчанию

        :return: keyboard's json"""
        buttoms = get_commands_from_text(DEFAULT_ANSWER)
        keyboard = self.set_keyboard_buttons(buttoms)
        return keyboard.get_keyboard()

    @staticmethod
    def __add_restart_button(keyboard: VkKeyboard) -> None:
        """"Добавляет в существующую клавиатуру кнопку с командой '/restart' """
        keyboard.add_line()
        keyboard.add_button(label=RESTART_COMMAND, color=VkKeyboardColor.SECONDARY)


keyboards = _Keyboard()
