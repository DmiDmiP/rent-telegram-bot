from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
import aiogram.utils.markdown as md
from aiogram.utils.emoji import emojize

from telegram_bot.misc import dp

bt_start = InlineKeyboardButton(text='Getting started?', callback_data='start')
kb1 = InlineKeyboardMarkup().add(bt_start)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hello. \nIf you give me information on the counters, I will tell you how much money you need "
                         "to send. \nHow does everything work here? Click /help", reply_markup=kb1)


@dp.message_handler(commands=['help'])
async def send_welcome(msg: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await msg.reply(f"Hi {msg.chat.username}! \nI created a bot so that you can find out how much money I need "
                    f"to transfer and not wait for me to count from the pictures. \n"
                    f"You need to start with the word /start.\n"
                    f"I made it as convenient and understandable as possible. You just need to enter numbers when "
                    f"answering questions. \n"
                    f"If you don't want to continue writing data, just write Stop and cancel everything.")


@dp.message_handler(regexp='Hello')
async def hello(message: types.Message):
    '''
    sends a response if you say hello
    '''
    await message.answer(f'And hello to you, if you are not joking! 😝')


@dp.message_handler()
async def echo(msg: types.Message):
    '''
    echo bot
    '''
    await msg.answer(f'I do not need "{msg.text}". I need /start')


@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(msg: types.Message):
    '''
    echo bot for not message
    '''
    message_text = md.text(emojize('I do not know what to do about it :astonished:'),
                           md.italic('\nI will just remind,'), 'you that there',
                           md.code('is a command'), '/help')
    await msg.reply(message_text, parse_mode=types.ParseMode.MARKDOWN)
