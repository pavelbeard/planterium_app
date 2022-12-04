import asyncio
import yaml
from telebot import types
from bot import bot_base, main_menu_handler, lvl_one_menu_handler


@bot_base.bot.message_handler(commands='start help'.split())
async def main(msg: types.Message):
    """Вызывает главное меню и меню поддержки"""
    match msg.text:
        case '/start':
            await bot_base.bot.send_message(
                chat_id=msg.chat.id,
                text='hello',
                reply_markup=bot_base.main_menu.assemble_keyboard()
            )
        case '/help':
            pass


@bot_base.bot.callback_query_handler(func=lambda call: call.data in bot_base.main_menu.cb_data)
async def main_menu(call: types.CallbackQuery):
    """Обрабатывает данные коллбэков из главного меню"""
    await main_menu_handler(bot_base=bot_base, call=call)


@bot_base.bot.callback_query_handler(func=lambda call: call.data in bot_base.back.cb_data)
async def main_menu(call: types.CallbackQuery):
    """Обрабатывает данные коллбэков из главного меню"""
    await lvl_one_menu_handler(bot_base=bot_base, call=call)


if __name__ == '__main__':
    asyncio.run(bot_base.bot.polling(none_stop=True, timeout=60))
