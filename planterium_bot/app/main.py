import asyncio
import os

from telebot import async_telebot, types
from bot.handlers import (
    MainCommandHandler,
    LevelOneCallbackHandler,
    LevelTwoCallbackHandler,
    LevelThreeCallbackHandler,
    cb_main_btns,
    cb_catalog_btns,
    cb_plants_btns,
    cb_contact_btns,
)
from bot.keyboard import CommandsBase

# сам бот
b = async_telebot.AsyncTeleBot(os.environ['API_KEY_PLANTERIUM_BOT'])

# настраиваем меню команд
commands = CommandsBase(b, commands={'start': 'Перезапуск бота'})


# main handler
@b.message_handler(content_types=['text'])
@b.message_handler(commands=commands.gen_commands())
async def command_handler(msg) -> None:
    """
    Создает основное меню\n
    :param msg: Объект Message, необходимый для работы бота
    :return: None
    """
    main_handler = MainCommandHandler(bot=b, message=msg)
    await main_handler.handler()


# обработчик меню первого уровня
@b.callback_query_handler(func=lambda call: call.data in cb_main_btns)
async def lvl_one_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по основному меню - меню 1 уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelOneCallbackHandler(bot=b, callback_query=call)
    await handler.handler()


# обработчик меню второго уровня
@b.callback_query_handler(func=lambda call: call.data in cb_contact_btns + cb_catalog_btns)
async def lvl_two_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по меню 2-го уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelTwoCallbackHandler(bot=b, callback_query=call)
    await handler.handler()


# обработчик меню третьего уровня
@b.callback_query_handler(func=lambda call: call.data in cb_plants_btns)
async def lvl_three_callback_handler(call: types.CallbackQuery) -> None:
    """
    Метод, позволяющий ходить по меню 3-го уровня\n
    :param call: callback, который содержит в себе информацию о кнопках:
    :return: None
    """
    handler = LevelThreeCallbackHandler(bot=b, callback_query=call)
    await handler.handler()


if __name__ == '__main__':
    asyncio.run(b.polling(none_stop=True, timeout=5))
