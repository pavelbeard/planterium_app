from abc import abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from telebot.async_telebot import AsyncTeleBot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton


@dataclass(init=True)
class CommandsBase:
    """
    Класс, создающий список команд
    """
    bot: AsyncTeleBot
    commands: dict

    def gen_commands(self) -> list:
        """
        Метод, создающий команды для бота\n
        :return: Возвращает объект list
        """
        commands = [BotCommand(command, description) for command, description in self.commands.items()]
        self.bot.set_my_commands(commands)
        return list(self.commands.keys())


@dataclass(init=True)
class KeyboardTitlesBase:
    """
    Базовый класс для клавиатуры
    """
    main_menu_btns: namedtuple
    contacts_menu_btns: namedtuple
    catalog_menu_btns: namedtuple
    plants_menu_btns: namedtuple


@dataclass(init=True)
class KeyboardConstructor(KeyboardTitlesBase):
    """
    Класс-конструктор для клавиатур Reply, Inline, ForcedReply и тд
    """

    @abstractmethod
    def gen_main_menu_markup(self):
        """
        Абстрактный метод. В классах-наследниках реализует главное меню.\n
        """
        pass

    @abstractmethod
    def gen_catalog_menu_markup(self):
        """
        Абстрактный метод. В классах-наследниках реализует меню каталога.\n
        """
        pass

    @abstractmethod
    def gen_contacts_menu_markup(self):
        """
        Абстрактный метод. В классах-наследниках реализует меню контактов.\n
        """
        pass

    @abstractmethod
    def gen_back_btns_markup(self, previous_lvl):
        """
        Абстрактный метод. В классах-наследниках реализует кнопки "Назад" и "В главное меню"
        """


# region ReplyKeyboardMarkup
# class ReplyKeyboardConstructor(KeyboardConstructor):
#     def __init__(
#             self,
#             # base tuples
#             main_btns: namedtuple,
#             contacts_btns: namedtuple,
#             # btn titles
#             main_btn_titles: tuple,
#             contacts_btn_title: tuple,
#     ):
#         super().__init__(main_btns, contacts_btns)
#
#     @property
#     def get_main_btns(self) -> namedtuple:
#         """
#         Именованый кортеж с названиями кнопок для главного меню\n
#         about: "О Planterium'e"\n
#         contacts: 'Контакты'\n
#         catalog: 'Каталог'\n
#         how_to_order: 'Как заказать'\n
#         guides: 'Уход за зелеными питомцами'\n
#         discounts: 'Скидки'\n
#         discounts: 'Скидки'\n
#         sales: 'Распродажи'\n
#         back: 'Назад'\n
#         :return: Возвращает объект namedtuple
#         """
#         return self.main_menu_btns
#
#     @property
#     def get_contact_btns(self) -> namedtuple:
#         """
#         Словарь с названиями кнопок для меню связи с владельцем Planterium\n
#         ig: 'Зеленый Instagram🌲'\n
#         tg: 'Зеленый Telegram🌵'\n
#         owner: 'Леша, Король джунглей🌴\n
#         :return: Возвращает объект namedtuple
#         """
#         return self.contacts_menu_btns
#
#     def gen_main_menu(self) -> ReplyKeyboardMarkup:
#         """
#         Функция, которая генерирует разметку для меню\n
#         :return: Возвращает объект ReplyKeyboardMarkup
#         """
#         markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
#
#         main_btns = self.get_main_btns
#
#         # first row
#         first_row = [KeyboardButton(main_btns.about), KeyboardButton(main_btns.contacts)]
#         # second row
#         second_row = [KeyboardButton(main_btns.catalog), KeyboardButton(main_btns.how_to_order)]
#         # third row
#         third_row = [KeyboardButton(main_btns.guides)]
#         # forth row
#         forth_row = [KeyboardButton(main_btns.discounts),
#                      KeyboardButton(main_btns.discounts), KeyboardButton(main_btns.sales)]
#
#         # gathering rows
#         markup.row(*first_row).row(*second_row).row(*third_row).row(*forth_row)
#
#         return markup
#
#     def gen_contacts_menu(self) -> ReplyKeyboardMarkup:
#         """
#         Генерирует клаиватуру для команды /contacts\n
#         :return: Возвращает объект ReplyKeyboardMarkup
#         """
#         contacts_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#
#         # именованный кортеж с названиями кнопок для раздела контактов
#         contact_btns = self.get_contact_btns
#         # именованный кортеж с названиями кнопок для главного меню
#         main_btns = self.get_main_btns
#
#         # вторая строка
#         second_row = [KeyboardButton(contact_btns.ig), KeyboardButton(contact_btns.tg)]
#
#         # первая строка и третья строка
#         contacts_markup.row(*[KeyboardButton(contact_btns.owner)]).row(
#             *second_row).row(*[KeyboardButton(main_btns.back)])
#
#         return contacts_markup
# endregion


class InlineKeyboardConstructor(KeyboardConstructor):
    """
    Вариант реализации клавиатуры через inline стиль
    """

    def __init__(
            self,
            # base tuples
            main_menu_btns: namedtuple,
            contacts_menu_btns: namedtuple,
            catalog_menu_btns: namedtuple,
            plants_menu_btns: namedtuple,
            # btn titles
            main_menu_btns_titles: tuple,
            contacts_menu_btns_titles: tuple,
            catalog_menu_btns_titles: tuple,
            plants_menu_btns_titles: tuple
    ):
        super().__init__(
            main_menu_btns,
            contacts_menu_btns,
            catalog_menu_btns,
            plants_menu_btns,
        )

        # сборка кнопок
        self.__main_menu_btns_class = self.main_menu_btns(*main_menu_btns_titles)  # главное меню
        self.__contacts_menu_btns_class = self.contacts_menu_btns(*contacts_menu_btns_titles)  # контакты
        self.__catalog_menu_btns_class = self.catalog_menu_btns(*catalog_menu_btns_titles)  # каталог
        self.__plants_menu_btns_class = self.plants_menu_btns(*plants_menu_btns_titles)  # кнопки в
        # категории "растения"

    @property
    def get_main_menu_class(self) -> namedtuple:
        """
        Готовое главное меню
        :return: namedtuple
        """
        return self.__main_menu_btns_class

    @property
    def get_contacts_menu_class(self) -> namedtuple:
        """
        Готовый раздел "Контакты"
        :return: namedtuple
        """
        return self.__contacts_menu_btns_class

    @property
    def get_catalog_menu_class(self) -> namedtuple:
        """
        Готовый раздел "Каталог"
        :return: namedtuple
        """
        return self.__catalog_menu_btns_class

    @property
    def get_plants_menu_class(self) -> namedtuple:
        """
        Готовый раздел "Растения"
        :return: namedtuple
        """
        return self.__plants_menu_btns_class

    def get_fields(self, named_tuple: namedtuple) -> namedtuple:
        """
        Выдает поля именованных кортежей
        :param named_tuple: Кортеж для обработки
        :return: namedtuple
        """
        fields = named_tuple._fields
        Tmp = namedtuple('Tmp', fields)
        return Tmp(*fields)

    # region Main menu
    def gen_main_menu_markup(self) -> InlineKeyboardMarkup:
        """
        Функция, которая генерирует разметку для меню\n
        :return: Возвращает объект InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup(row_width=3)

        main_btns = self.__main_menu_btns_class
        callback_data = self.get_fields(self.main_menu_btns)

        # first row
        first_row = [
            InlineKeyboardButton(main_btns.about, callback_data=callback_data.about),
        ]
        # second row
        second_row = [
            InlineKeyboardButton(main_btns.catalog, callback_data=callback_data.catalog),
            InlineKeyboardButton(main_btns.how_to_order, callback_data=callback_data.how_to_order),
        ]
        # third row
        third_row = [
            InlineKeyboardButton(main_btns.guides, callback_data=callback_data.guides),
            InlineKeyboardButton(main_btns.soil_recipe, callback_data=callback_data.soil_recipe),
        ]
        # forth row
        forth_row = [
            InlineKeyboardButton(main_btns.discounts, callback_data=callback_data.discounts),
        ]
        # fifth row
        fifth_row = [
            InlineKeyboardButton(main_btns.services, callback_data=callback_data.services),
            InlineKeyboardButton(main_btns.greening, callback_data=callback_data.greening),
        ]
        # sixth row
        sixth_row = [
            InlineKeyboardButton(main_btns.contacts, callback_data=callback_data.contacts),
            InlineKeyboardButton(main_btns.partnership, callback_data=callback_data.partnership),
        ]
        # # seventh row
        # seventh_row = [
        #     InlineKeyboardButton()
        # ]

        markup.row(*first_row).row(*second_row).row(*third_row).row(*forth_row).row(*fifth_row).row(
            *sixth_row
        )
        return markup

    def gen_back_btns_markup(self, back_to: str = None) -> InlineKeyboardMarkup:
        """
        Генерирует кнопки 'Назад' и 'В главное меню'\n
        :param back_to: Предыдущий уровень меню, параметр принимает информацию
        о коллбэке из кортежа коллбэков
        :return: InlineKeyboardMarkup
        """
        # главное меню
        main_btns = self.__main_menu_btns_class
        main_cb_data = self.get_fields(self.main_menu_btns)

        #
        if back_to is None:
            return InlineKeyboardMarkup().row(*[InlineKeyboardButton(main_btns.back,
                                                                     callback_data=main_cb_data.in_main_menu)])

        return InlineKeyboardMarkup().row(
            *[InlineKeyboardButton(main_btns.back, callback_data=back_to),
              InlineKeyboardButton(main_btns.in_main_menu, callback_data=main_cb_data.in_main_menu)])
    # endregion

    # region Catalog menu
    def gen_catalog_menu_markup(self) -> InlineKeyboardMarkup:
        """
        Генерирует меню каталога\n
        :return: InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup()

        catalog_btns = self.__catalog_menu_btns_class
        catalog_cb_data = self.get_fields(self.catalog_menu_btns)

        back_btns = self.gen_back_btns_markup()

        # first row
        first_row = [
            InlineKeyboardButton(catalog_btns.plants, callback_data=catalog_cb_data.plants),
            InlineKeyboardButton(catalog_btns.pots, callback_data=catalog_cb_data.pots),
        ]

        return markup.row(*first_row).row(*[InlineKeyboardButton(
            catalog_btns.soil, callback_data=catalog_cb_data.soil
        )]).row(*back_btns.keyboard[0])

    def gen_list_of_plants(self) -> InlineKeyboardMarkup:
        """
        На основе данных о количестве растений из базы данных генерирует список кнопок\n
        Пока тестовая функция\n
        :return: InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup()

        plants_btns = self.__plants_menu_btns_class
        plants_cb_data = self.get_fields(self.plants_menu_btns)

        cb_data = self.get_fields(self.main_menu_btns)
        back_btns = self.gen_back_btns_markup(cb_data.catalog)

        first_row = [InlineKeyboardButton(x, callback_data=y) for x, y in zip(plants_btns._fields, plants_cb_data)]

        return markup.row(*first_row).row(*back_btns.keyboard[0])

    # endregion

    # region Contacts menu
    def gen_contacts_menu_markup(self) -> InlineKeyboardMarkup:
        """
        Генерирует клаиватуру для команды /contacts\n
        :return: Возвращает объект InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup()

        # главное меню
        main_btns = self.__main_menu_btns_class
        main_cb_data = self.get_fields(self.main_menu_btns)

        # раздел "контакты"
        contact_btns = self.__contacts_menu_btns_class
        contacts_cb_data = self.get_fields(self.contacts_menu_btns)

        # first row
        first_row = [InlineKeyboardButton(contact_btns.owner, callback_data=contacts_cb_data.owner)]
        # second row
        second_row = [
            InlineKeyboardButton(contact_btns.ig, callback_data=contacts_cb_data.ig),
            InlineKeyboardButton(contact_btns.tg, callback_data=contacts_cb_data.tg)
        ]
        # third row
        third_row = [InlineKeyboardButton(main_btns.back, callback_data=main_cb_data.back)]

        return markup.row(*first_row).row(*second_row).row(*third_row)

    def gen_instagram_btn_markup(self) -> InlineKeyboardMarkup:
        """
        Кнопка инсты
        :return: InlineKeyboardMarkup
        """
        cb_data = self.get_fields(self.main_menu_btns)
        back_btns = self.gen_back_btns_markup(cb_data.contacts)

        return InlineKeyboardMarkup().row(*[
            InlineKeyboardButton("Подписаться",
                                 url='instagram.com/planterium.moscow')
        ]).row(*back_btns.keyboard[0])

    def gen_telegram_btn_markup(self) -> InlineKeyboardMarkup:
        """
        Кнопка телеги
        :return: InlineKeyboardMarkup
        """
        cb_data = self.get_fields(self.main_menu_btns)
        back_btns = self.gen_back_btns_markup(cb_data.contacts)

        return InlineKeyboardMarkup().row(*[
            InlineKeyboardButton("Присоединиться!",
                                 url='https://t.me/planteriummoscow')
        ]).row(*back_btns.keyboard[0])

    def gen_owner_btn_markup(self) -> InlineKeyboardMarkup:
        cb_data = self.get_fields(self.main_menu_btns)
        back_btns = self.gen_back_btns_markup(cb_data.contacts)

        return InlineKeyboardMarkup().row(*[
            InlineKeyboardButton("Написать",
                                 url='https://t.me/stalmt')
        ]).row(*back_btns.keyboard[0])

    # endregion
