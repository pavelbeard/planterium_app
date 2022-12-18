import asyncio
import os
import unittest

from telebot import types
from telebot.async_telebot import AsyncTeleBot


class TestPytelegramApiBot(unittest.TestCase):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    API_KEY = os.getenv('API_KEY_PLANTERIUM_BOT')

    markup = InlineKeyboardMarkup().row(*[
        InlineKeyboardButton('Test pic 1', callback_data='test_pic_1'),
        InlineKeyboardButton('Test pic 2', callback_data='test_pic_2'),
        InlineKeyboardButton('Test pic 3', callback_data='test_pic_3'),
        InlineKeyboardButton('Test pic 4', callback_data='test_pic_4'),
        InlineKeyboardButton('Test pic 5', callback_data='test_pic_5'),
        InlineKeyboardButton('Test link 1', callback_data='test_link_1')
    ]).row(*[InlineKeyboardButton('Back to main menu', callback_data='main_menu')])

    new_markup = InlineKeyboardMarkup(row_width=5).row(*[
        InlineKeyboardButton('1', callback_data='one'),
        InlineKeyboardButton('2', callback_data='two'),
        InlineKeyboardButton('3', callback_data='three'),
        InlineKeyboardButton('4', callback_data='four'),
        InlineKeyboardButton('5', callback_data='five'),
    ])

    def test_bot(self):
        from telebot import async_telebot, types
        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

        bot = async_telebot.AsyncTeleBot(self.API_KEY)


        async def main_menu(message: types.Message, callback=False):
            main_menu_title = 'Main menu'
            if not callback:
                await bot.send_message(
                    message.chat.id,
                    main_menu_title,
                    reply_markup=self.markup
                )
            else:
                await bot.edit_message_text(
                    main_menu_title,
                    message.chat.id,
                    message.id,
                    reply_markup=self.markup
                )

        @bot.message_handler(commands=['start', 'test'])
        @bot.message_handler(content_types=['text'])
        async def cmd_handler(msg: types.Message):
            match msg.text:
                case '/start':
                    await main_menu(msg)

        @bot.callback_query_handler(func=lambda call: True)
        async def callback_test(call: types.CallbackQuery):
            path = os.path.join("C:\\", 'users', 'pavel', 'downloads', 'telegram desktop',
                                'photo_2022-11-05_13-22-28.jpg')
            with open(path, 'rb') as p:
                photo = types.InputMediaPhoto(p.read(), caption='photo is edited')

            match call.data:
                case 'test_pic_1':
                    url = "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE53m9O?ver" \
                          "=ec1e "
                    await bot.edit_message_text(
                        f'[picture]({url})', call.message.chat.id, call.message.id, parse_mode='MarkdownV2',
                        reply_markup=self.new_markup
                    )
                case 'test_pic_2':
                    await bot.send_photo(chat_id=call.message.chat.id, photo=photo.media, caption='test')
                case 'test_pic_4':
                    await bot.edit_message_text(
                        "<a href='https://cdn.britannica.com/02/9002-004-4C653566/toothwort.jpg?s"
                        "=1500x700&q=85'>link to Pic</a>",
                        call.message.chat.id, call.message.id, parse_mode='html',
                        reply_markup=InlineKeyboardMarkup().row(*[
                            InlineKeyboardButton('Main menu', callback_data='main_menu')
                        ]))
                case 'main_menu':
                    await main_menu(message=call.message, callback=True)
                case 'test_link_1':
                    await bot.edit_message_text(
                        "<a href='https://phoenixnap.com/kb/wp-content/uploads/2021/04/hot-to-install-and-configure"
                        "-nginx-on-ubuntu-02.png'>&#8205;</a>Test",
                        call.message.chat.id, call.message.id, parse_mode='html',
                        reply_markup=InlineKeyboardMarkup().row(*[
                            InlineKeyboardButton('Main menu', callback_data='main_menu')
                        ]))
                case 'one':
                    url = 'http://127.0.0.1:8000/get_plants/1'
                    await bot.edit_message_text(
                        f'[picture]({url})', call.message.chat.id, call.message.id, parse_mode='MarkdownV2',
                        reply_markup=InlineKeyboardMarkup().row(*[
                            InlineKeyboardButton('Main menu', callback_data='main_menu')
                        ]),
                        disable_web_page_preview=False
                    )
                case 'test_pic_5':
                    pass

        asyncio.run(bot.polling(none_stop=True, timeout=5))

    def test_bot_sync(self):
        import telebot
        from telebot import types
        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

        bot = telebot.TeleBot(self.API_KEY)

        def main_menu(message: types.Message, handle_type: int = 0):
            """
            Calls main menu\n
            :param message: object of types.Message
            :param handle_type: function for choice: 1 - send_message\n
            2 - edit_message_text
            3 - edit_caption
            :return:
            """
            text = "Hello! It's a keyboard!"

            match handle_type:
                case 1:
                    bot.send_message(message.chat.id, text,
                                     reply_markup=self.markup)
                case 2:
                    bot.edit_message_text(text, message.chat.id, message.id,
                                          reply_markup=self.markup)
                case 3:
                    bot.edit_message_caption(text, message.chat.id, message.id,
                                             reply_markup=self.markup)

        @bot.message_handler(content_types=['text'])
        @bot.message_handler(commands=['start', 'help'])
        def main(message: types.Message):
            match message.text:
                case '/start':
                    main_menu(message, 1)
                case '/help':
                    bot.send_message(
                        message.chat.id, 'help',
                        reply_markup=InlineKeyboardMarkup(row_width=3).row(*[
                            InlineKeyboardButton('Back to main menu', 'main_menu')
                        ])
                    )

        @bot.callback_query_handler(func=lambda call: True)
        def cb_handler(call: types.CallbackQuery):
            match call.data:
                case 'main_menu':
                    main_menu(call.message, 2)
                case 'main_menu_2':
                    main_menu(call.message, 3)
                # edit message - not work
                case 'test_pic_1':
                    bot.edit_message_text("<a href='http://127.0.0.1:8000/get_plants/1'>testpic</a>",
                                          call.message.chat.id, call.message.id,
                                          reply_markup=InlineKeyboardMarkup(row_width=3).row(*[
                                              InlineKeyboardButton('Back to main menu', callback_data='main_menu')
                                          ]), parse_mode='HTML')
                case 'test_pic_2':
                    pass

        bot.infinity_polling(timeout=60)


class TestNewKeyboard(unittest.TestCase):
    class NewKeyboard:
        def __init__(self, btns_base: list[str | tuple], btns_titles: list[str | tuple]):
            self.btns_base = btns_base
            self.btns_titles = btns_titles

        def assemble_keyboard(self) -> types.InlineKeyboardMarkup:
            # base = self.btns_base
            # base_rows = json.dumps([b._fields for base in base for b in base])
            #
            # titles = self.btns_titles
            # titles_rows = json.dumps([t for titles in titles for t in titles])
            #
            # markup = InlineKeyboardMarkup(row_width=3).
            btns = zip(self.btns_base, self.btns_titles)

            keyboard = []

            for keys, values in btns:
                if type(keys) is not tuple and type(values) is not tuple:
                    keyboard.append(types.InlineKeyboardButton(callback_data=keys, text=values))
                else:
                    row = []
                    for k, v in zip(keys, values):
                        row.append(types.InlineKeyboardButton(callback_data=k, text=v))

                    keyboard.append(row)

            return types.InlineKeyboardMarkup(*[keyboard])

    def test_startup(self):
        kb = self.NewKeyboard(
            # first set
            btns_base=[
                'about',
                ('catalog', 'how_to_order'),
                ('guides', 'soil_recipe'),
                'discounts',
                ('services', 'greening'),
                ('contacts', 'partnership'),
                ('back', 'to_main_menu')
            ],
            btns_titles=[
                "О Planterium'e🪴",
                ('Каталог🗒️', 'Как заказать❓'),
                ('Мини-гайды📕', 'Рецепты грунта📃'),
                'Скидки⚡',
                ('Спасение🚑', 'Озеленение🪴',),
                ('Контакты📱', 'Сотрудничество🤝'),
                ('Назад🔙', 'В главное меню📒'),
            ]
        )

        test = kb.assemble_keyboard()

        API_KEY = os.getenv('API_KEY_TEST_BOT')

        bot = AsyncTeleBot(token=API_KEY)

        @bot.message_handler(commands='start help')
        async def main(msg: types.Message):
            match msg.text:
                case '/start':
                    await bot.send_message(
                        chat_id=msg.chat.id,
                        text='hello',
                        reply_markup=test
                    )

        bot.infinity_polling(timeout=60, skip_updates=False)

        pass


if __name__ == '__main__':
    unittest.main()
