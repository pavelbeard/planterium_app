import logging.handlers

import yaml
import os
import os.path as os_path
from telebot import async_telebot
from .keyboard import InlineKeyboardConstructor


class Startup:
    """
    Класс-инициализатор бота\n
    Содержит в себе:
    \t- бот
    \t- главное меню
    \t- контакты
    """
    __API_KEY = os.getenv('API_KEY_PLANTERIUM_BOT', "5741189229:AAF9nka1wLsCKLOO81ETXfu1WGG_wyg3NgU")
    bot = async_telebot.AsyncTeleBot(token=__API_KEY)
    path = os.getenv("BOT_CONFIG_YML_PATH", os_path.join(
        "D:\\", "Pycharm", "sobes_projects", "sobes_projects",
        "planterium_app", "planterium_bot", "bot-config.yml"
    ))

    def __init__(self):
        #########################################
        ############# MAIN BTNS #################
        #########################################
        self.main_menu = InlineKeyboardConstructor(
            btns_base=(
                'about',
                ('catalog', 'how_to_order'),
                ('guides', 'soil_recipe'),
                'discounts',
                ('services', 'greening'),
                ('contacts', 'partnership'),
            ),
            btns_titles=(
                "О Planterium'e🪴",
                ('Каталог🗒️', 'Как заказать❓'),
                ('Мини-гайды📕', 'Рецепты грунта📃'),
                'Скидки⚡',
                ('Спасение🚑', 'Озеленение🪴',),
                ('Контакты📱', 'Сотрудничество🤝'),
            )
        )  # sss
        self.back = InlineKeyboardConstructor(
            btns_base=('back',),
            btns_titles=('Назад🔙',)
        )
        self.to_main_menu = InlineKeyboardConstructor(
            btns_base=('to_main_menu',),
            btns_titles=('В главное меню📒',)
        )
        #########################################

        self.catalog_menu = InlineKeyboardConstructor(
            btns_base=(('plants', 'pots'), 'soil'),
            btns_titles=(('Растения🌺', 'Горшки🪴'), 'Грунт💰')
        )
        self.contacts_menu = InlineKeyboardConstructor(
            btns_base=(('ig', 'tg'), 'owner'),
            btns_titles=(('Зеленый Instagram🌲', 'Зеленый Telegram🌵'),
                         'Леша, Король джунглей🌴'),
            url1='https://instagram.com/planterium.moscow', url2='https://t.me/planteriummoscow',
            url3='https://t.me/stalmt'
        )
        self.admin_menu = InlineKeyboardConstructor(
            btns_base=(('edit_about', 'edit_catalog'),),
            btns_titles=(("""Edit "О Planterium'e🪴""", "Редактировать каталог"),)
        )

        ###### EDIT CATALOG MENU ######
        self.edit_plants_menu = InlineKeyboardConstructor(
            btns_base=((),),
            btns_titles=((),)
        )

    def get_plants_for_keyboard(self):
        # TODO: реализвать функцию заполнения клавиатуры
        self.edit_plants_menu
        pass

    @classmethod
    def get_config(cls) -> {}:
        try:
            file = open(cls.path, 'r')
        except FileNotFoundError as err:
            print(err)
            exit(1)
        else:
            with file as config:
                return yaml.safe_load(config)

    @classmethod
    def set_config(cls, data: dict):
        """
        Сохраняет данные в конфиг
        :param data: Данные для записи в конфиг
        :return: None
        """
        try:
            file = open(cls.path, 'w')
            old_file = open(cls.path, 'r')
        except FileNotFoundError as err:
            print(err)
            return False
        else:
            with file as f, old_file as old_f:
                # TODO: разобраться с чертовой КОДИРОВКОЙ!!!!1111111

                old_data = yaml.safe_load(old_f)
                new_data = old_data.get('settings')
                new_data.update(data)
                yaml.dump(stream=f, data=new_data, sort_keys=False, default_flow_style=False, encoding='cp1252')
                return True


bot_base = Startup()
bot = bot_base.bot
