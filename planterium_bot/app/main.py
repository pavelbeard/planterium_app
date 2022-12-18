import asyncio

from telebot import types
from bot_app import bot_base
from bot_app import main_menu_handler, lvl_one_menu_handler, request_to_check_admin, welcome_msg
from bot_app.startup import bot as planterium_bot


@planterium_bot.message_handler(commands='start help admin'.split())
async def main(msg: types.Message):
    """Вызывает главное меню, меню поддержки и админскую клавиаутуру, если юзер имеет доступ к ней"""
    match msg.text:
        case '/start':
            await planterium_bot.send_message(
                chat_id=msg.chat.id,
                text=welcome_msg(first_name=msg.chat.first_name, last_name=msg.chat.last_name),
                reply_markup=bot_base.main_menu.assemble_keyboard()
            )
        case '/help':
            pass
        case '/admin':
            result = await request_to_check_admin(msg.from_user.id)
            admin_markup = bot_base.admin_menu.assemble_keyboard()
            is_admin, reply_markup = ("Интерфейс администратора", admin_markup) if result else ('Нет доступа', None)
            await planterium_bot.send_message(chat_id=msg.chat.id, text=is_admin, reply_markup=reply_markup)


@bot_base.bot.callback_query_handler(func=lambda call: call.data in bot_base.main_menu.cb_data)
async def main_menu(call: types.CallbackQuery):
    """Обрабатывает данные коллбэков из главного меню"""
    await main_menu_handler(bot_base=bot_base, call=call)


@bot_base.bot.callback_query_handler(func=lambda call: call.data in bot_base.back.cb_data)
async def lvl_one_menu(call: types.CallbackQuery):
    """Обрабатывает данные коллбэков из главного меню"""
    await lvl_one_menu_handler(bot_base=bot_base, call=call)


if __name__ == '__main__':
    asyncio.run(bot_base.bot.polling(none_stop=True, timeout=60))
