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
            btns_titles=(("""Редактировать "О Planterium'e🪴""", "Редактировать каталог"),)
        )

    @staticmethod
    def get_config() -> {}:
        path = os.getenv("BOT_CONFIG_YML_PATH", os_path.join(
            "D:\\", "Pycharm", "sobes_projects", "sobes_projects",
            "planterium_app", "planterium_bot", "bot-config.yml"
        ))
        try:
            file = open(path, 'r')
        except FileNotFoundError as err:
            print(err)
            exit(1)
        else:
            with file as config:
                return yaml.safe_load(config)


bot_base = Startup()
bot = bot_base.bot
