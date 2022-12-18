import json

from telebot.types import CallbackQuery
from aiohttp import client
from .startup import Startup


def welcome_msg(**kwargs) -> str:
    """
    Приветственное сообщение
    :return: str
    """
    fname = kwargs.get('first_name')
    lname = " " + kwargs.get('last_name') if kwargs.get('last_name') is not None else ""
    return f"Привет {fname}{lname}, Я бот-помощник Planterium!\nДавай помогу тебе😉\n" \
           f"Сделаю твою жизнь чуточку зеленее🙃"


async def main_menu_handler(bot_base: Startup, call: CallbackQuery):
    """
    Обработчик главного меню\n
    :param bot_base: Инстанс инициализатора
    :param call: очередь коллбэков
    """

    match call.data:
        case 'about':
            pass
        case 'catalog':
            pass
        case 'how_to_order':
            pass
        case 'guides':
            pass
        case 'soil_recipe':
            pass
        case 'discounts':
            pass
        case 'service':
            pass
        case 'greening':
            pass
        case 'contacts':
            await bot_base.bot.edit_message_text(
                text='Контакты📱', chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=bot_base.contacts_menu.assemble_keyboard().row(
                    *bot_base.back.assemble_keyboard().keyboard[0]))
        case 'partnership':
            pass


async def admin_menu_handler(bot_base: Startup, call: CallbackQuery):
    """
    Обработчик интерфейса администратора.\n
    :param bot_base: Инстанс инициализатора.
    :param call: очередь коллбэков.
    """
    match call.data:
        case 'back':
            await bot_base.bot



async def lvl_one_menu_handler(bot_base: Startup, call: CallbackQuery):
    """
    Обработчик меню первого уровня: "о владельце", "контакты"\n
    :param bot_base: Инстанс инициализатора.
    :param call: очередь коллбэков.
    """
    match call.data:
        case 'back':
            # главное меню
            await bot_base.bot.edit_message_text(welcome_msg(
                    first_name=call.message.chat.first_name, last_name=call.message.chat.last_name),
                chat_id=call.message.chat.id, message_id=call.message.message_id,
                reply_markup=bot_base.main_menu.assemble_keyboard()
            )


async def request_to_check_admin(user_id: int) -> bool:
    """
    Запрос на проверку прав администратора
    :param user_id: ID юзера - ключ к админке
    :return: True - если id есть базе данных админов, иначе False
    """
    url = Startup.get_config().get('settings').get('api_url') + "/api/check_admin"
    headers = {"Content-Type": "application/json;charset=utf8"}
    user_data = json.dumps({"user_id": str(user_id)})

    async with client.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=user_data) as response:
            data = await response.json()
            return data.get('check_admin')
