import os
from collections import namedtuple
from dataclasses import dataclass
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from .keyboard import InlineKeyboardConstructor

# собираем клаву
kb = InlineKeyboardConstructor(
    # МЕНЯЕШЬ СПИСОК КНОПОК - НЕ ЗАБУДЬ ПОМЕНЯТЬ В ФУНКЦИИ gen!
    main_menu_btns=namedtuple(
        'MainBtns',
        """about 
        catalog how_to_order 
        guides soil_recipe 
        discounts 
        services greening 
        contacts partnership       
        back in_main_menu"""  # 7 rows
    ),
    catalog_menu_btns=namedtuple(
        'CatalogBtns', 'plants pots soil'
    ),
    plants_menu_btns=namedtuple(
        'PlantsBtns', 'one two three'
    ),
    contacts_menu_btns=namedtuple(
        'ContactBtns', 'ig tg owner'
    ),
    main_menu_btns_titles=(
        "О Planterium'e🪴",  # 1
        'Каталог🗒️', 'Как заказать❓',  # 2
        'Мини-гайды📕', 'Рецепты грунта📃',  # 3
        'Скидки⚡',  # 4
        'Спасение🚑', 'Озеленение🪴',  # 5
        'Контакты📱', 'Сотрудничество🤝',  # 6
        'Назад🔙', 'В главное меню📒'
    ),
    catalog_menu_btns_titles=(
        'Растения🌺', 'Горшки🪴',  # 1
        'Грунт💰'  # 2
    ),
    plants_menu_btns_titles=(
        '1', '2', '3'
    ),
    contacts_menu_btns_titles=(
        'Зеленый Instagram🌲', 'Зеленый Telegram🌵',  # 2
        'Леша, Король джунглей🌴'  # 1
    )
)

# разметка
main_btns = kb.gen_main_menu_markup()
contact_btns = kb.gen_contacts_menu_markup()
catalog_btns = kb.gen_catalog_menu_markup()
plants_btns = kb.gen_list_of_plants()
owner_btn = kb.gen_owner_btn_markup()
ig_btn = kb.gen_instagram_btn_markup()
tg_btn = kb.gen_telegram_btn_markup()

# коллбэки
cb_main_btns = kb.get_fields(kb.main_menu_btns)
cb_catalog_btns = kb.get_fields(kb.catalog_menu_btns)
cb_plants_btns = kb.get_fields(kb.plants_menu_btns)
cb_contact_btns = kb.get_fields(kb.contacts_menu_btns)

# классы меню
main_menu_class = kb.get_main_menu_class
contact_menu_class = kb.get_contacts_menu_class
catalog_menu_class = kb.get_catalog_menu_class
plants_menu_class = kb.get_plants_menu_class


def welcome_msg(**kwargs) -> str:
    """
    Приветственное сообщение
    :return: str
    """
    fname = kwargs.get('first_name')
    lname = " " + kwargs.get('last_name') if kwargs.get('last_name') is not None else ""
    return f"Привет {fname}{lname}, Я бот-помощник Planterium!\nДавай помогу тебе😉\n" \
           f"Сделаю твою жизнь чуточку зеленее🙃"


@dataclass(init=True)
class MainCommandHandler:
    message: types.Message
    bot: AsyncTeleBot

    async def handler(self) -> None:
        """
        Обрабатывает команды при вызове пользователем, а так же случайно введенный текст\n
        Выводит главное меню\n
        :return: None
        """
        bot = self.bot
        message = self.message

        match self.message.text:
            case '/start':
                await bot.send_message(message.chat.id, welcome_msg(
                    first_name=message.chat.first_name, last_name=message.chat.last_name),
                                       reply_markup=kb.gen_main_menu_markup())
            case _:
                await bot.send_message(message.chat.id, 'Я тебя не понимаю(\nНажми кнопку или введи /start')


@dataclass(init=True)
class CallbackHandler:
    """Базовый класс для обработчиков кнопок"""
    bot: AsyncTeleBot
    callback_query: types.CallbackQuery

    async def handler(self) -> None:
        """Абстрактный метод обработчика callback"""
        pass


@dataclass(init=True)
class LevelOneCallbackHandler(CallbackHandler):
    """Класс, включающий в себя обработчик меню первого уровня"""

    async def handler(self) -> None:
        """
        Обрабатывает коллбэки при нажатии кнопки в меню первого уровня \n
        :return: None
        """
        bot = self.bot
        call = self.callback_query

        match call.data:
            # главное меню
            case cb_main_btns.in_main_menu | cb_main_btns.back:
                await bot.edit_message_text(
                    welcome_msg(first_name=call.message.chat.first_name, last_name=call.message.chat.last_name),
                    call.message.chat.id, call.message.id,
                    reply_markup=main_btns
                )
            # каталог
            case cb_main_btns.catalog:
                await bot.edit_message_text(
                    main_menu_class.catalog, call.message.chat.id, call.message.id,
                    reply_markup=catalog_btns
                )
            # контакты
            case cb_main_btns.contacts:
                await bot.edit_message_text(
                    main_menu_class.contacts, call.message.chat.id, call.message.id,
                    reply_markup=contact_btns
                )
            case _:
                await bot.send_message(call.message.chat.id, 'Nothing')


@dataclass(init=True)
class LevelTwoCallbackHandler(CallbackHandler):
    """Класс, включающий в себя обработчик меню второго уровня"""

    async def handler(self) -> None:
        """
        Обрабатывает коллбэки при нажатии кнопки в меню второго уровня \n
        :return: None
        """
        bot = self.bot
        call = self.callback_query

        match call.data:
            case cb_catalog_btns.plants:    # растения
                await bot.send_photo(
                    call.message.chat.id,
                    open(os.path.join('C:\\', 'users', 'pavel', 'downloads', 'RE53m9O.jpg'), 'rb'),
                    caption="test"
                )
                await bot.edit_message_text('test', call.message.chat.id, call.message.id,
                                            reply_markup=plants_btns)
                # await bot.edit_messa
                # await bot.edit_message_media(InputMediaPhoto(img, caption='test'),
                #                              call.message.chat.id, call.message.id)
            case cb_contact_btns.owner:  # owner
                await bot.edit_message_text(contact_menu_class.owner,
                                            call.message.chat.id, call.message.id,
                                            reply_markup=owner_btn)
            case cb_contact_btns.ig:  # instagram
                await bot.edit_message_text(contact_menu_class.ig,
                                            call.message.chat.id, call.message.id,
                                            reply_markup=ig_btn)
            case cb_contact_btns.tg:  # telegram
                await bot.edit_message_text(contact_menu_class.tg,
                                            call.message.chat.id, call.message.id,
                                            reply_markup=tg_btn)
            case cb_main_btns.back:  # back
                await bot.edit_message_text(main_menu_class.contacts, call.message.chat.id, call.message.id,
                                            reply_markup=contact_btns)


@dataclass(init=True)
class LevelThreeCallbackHandler(CallbackHandler):
    """Обрабатывает коллбэки третьего уровня меню"""
    async def handler(self) -> None:
        bot = self.bot
        call = self.callback_query

        match call.data:
            case cb_main_btns.back:
                await bot.edit_message_media(
                    media=None, chat_id=call.message.chat.id, message_id=call.message.id,
                    reply_markup=catalog_btns
                )


