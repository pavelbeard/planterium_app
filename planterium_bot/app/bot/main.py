import asyncio
import os

from telebot import async_telebot, types
from handlers import (
    MainCommandHandler,
    LevelOneCallbackHandler,
    LevelTwoCallbackHandler,
    LevelThreeCallbackHandler,
    cb_main_btns,
    cb_catalog_btns,
    cb_plants_btns,
    cb_contact_btns,
)
from keyboard import CommandsBase

# сам бот
bot = async_telebot.AsyncTeleBot(os.environ['API_KEY_PLANTERIUM_BOT'])

# настраиваем меню команд
commands = CommandsBase(bot, commands={'start': 'Перезапуск бота'})


# main handler
@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=commands.gen_commands())
async def command_handler(msg) -> None:
    """
    Создает основное меню\n
    :param msg: Объект Message, необходимый для работы бота
    :return: None
    """
    main_handler = MainCommandHandler(bot=bot, message=msg)
    await main_handler.handler()


# обработчик меню первого уровня
@bot.callback_query_handler(func=lambda call: call.data in cb_main_btns)
async def lvl_one_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по основному меню - меню 1 уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelOneCallbackHandler(bot=bot, callback_query=call)
    await handler.handler()


# обработчик меню второго уровня
@bot.callback_query_handler(func=lambda call: call.data in cb_contact_btns + cb_catalog_btns)
async def lvl_two_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по меню 2-го уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelTwoCallbackHandler(bot=bot, callback_query=call)
    await handler.handler()


# обработчик меню третьего уровня
@bot.callback_query_handler(func=lambda call: call.data in cb_plants_btns)
async def lvl_three_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по меню 3-го уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelThreeCallbackHandler(bot=bot, callback_query=call)
    await handler.handler()


if __name__ == '__main__':
    asyncio.run(bot.polling(none_stop=True, timeout=5))
