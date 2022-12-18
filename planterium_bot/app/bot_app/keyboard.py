from typing import Any
from telebot import types


class InlineKeyboardConstructor:
    """
    Класс конструктора динамической inline-клавиатуры!\n
    Может использоваться для создания любой навигации любой вложенности
    """

    def __init__(self, btns_base: tuple, btns_titles: tuple, **kwargs: Any):
        """
        Конструктор динамической inline-клавиатуры!\n
        Может использоваться для создания любой навигации любой вложенности\n
        :param btns_base: Список коллбэков кнопок. Используется как база
        :param btns_titles: Список тайтлов для кнопок
        :param kwargs: Используется для: url: str|login_url: str(порядковый номер кнопки). Пример: url1, login_url3 и тд
        """
        self.btns_base = btns_base
        self.btns_titles = btns_titles
        self.__kwargs = kwargs
        self.cb_data = []

        for base in btns_base:
            if type(base) is str:
                self.cb_data.append(base)
            else:
                self.cb_data += [b for b in base]

    def assemble_keyboard(self) -> types.InlineKeyboardMarkup:
        """
        Метод, конструирующий inline-клавиатуру\n
        :return: InlineKeyboardMarkup
        """
        btns = zip(self.btns_base, self.btns_titles)

        markup = types.InlineKeyboardMarkup()

        num = 1  # номер кнопки
        for keys, values in btns:
            if type(keys) is str and type(values) is str:
                markup.row(*[self.__construct_button(keys, values, num)])
                num += 1
            else:
                row = []
                for k, v in zip(keys, values):
                    row.append(self.__construct_button(k, v, num))
                    num += 1

                markup.row(*row)

        return markup

    def __construct_button(self, key: str, value: str, num: int) -> types.InlineKeyboardButton:
        """
        Вспомогательная функция конструирования кнопок\n
        :param key: Callback data
        :param value: Title кнопки
        :param num: Номер кнопки
        :return: InlineKeyboardButton
        """
        url = self.__kwargs.get(f'url{num}')
        login_url = self.__kwargs.get(f'login_url{num}')
        switch_inline_query = self.__kwargs.get(f'switch_inline_query{num}')
        switch_inline_query_current_chat = self.__kwargs.get(f'switch_inline_query_current_chat{num}')
        pay = self.__kwargs.get(f'pay{num}')
        web_app = self.__kwargs.get(f'web_app{num}')

        return types.InlineKeyboardButton(
            callback_data=key, text=value,
            url=url, login_url=login_url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            pay=pay,
            web_app=web_app
        )

