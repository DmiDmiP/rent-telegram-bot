from aiogram import executor
from telegram_bot.misc import dp

if __name__ == '__main__':
    ### Start boot polling
    executor.start_polling(dp, skip_updates=True)