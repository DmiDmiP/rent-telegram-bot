from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.emoji import emojize
import aiogram.utils.markdown as md
from telegram_bot.misc import dp, bot, ids, admin
import telegram_bot.handlers.count_engine as count_engine

bt_right = InlineKeyboardButton(text='Right?', callback_data='right')
bt_start = InlineKeyboardButton(text='No, again.', callback_data='not_right')
kb = InlineKeyboardMarkup().add(bt_right, bt_start)


class Form(StatesGroup):
    gas_num = State()
    gas_rub = State()
    water = State()
    el1 = State()
    el2 = State()


class AddForm(StatesGroup):
    add_mouth = State()
    add_gas = State()


def is_number(msg):
    '''
    check is number
    '''
    try:
        float(msg)
        return True
    except ValueError:
        return False


@dp.callback_query_handler(lambda c: c.data == 'not_right')
@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_callback_button1(callback_query: types.CallbackQuery):
    '''
    ask of gas
    '''
    await bot.answer_callback_query(callback_query.id)
    if callback_query.from_user.id in ids:
        await Form.gas_num.set()
        await bot.send_message(callback_query.from_user.id, 'Getting started.\nSend me the numbers on the gas meter to '
                                                            'the point.')
    else:
        # if user not in right ids, send messege to admin
        await bot.send_message(callback_query.from_user.id, md.text(
            f'Привет {callback_query.from_user.first_name}.\nI do not know if you live in the owner is apartment, but '
            f'I will send your data to him. If anything, he will write to you. {emojize(":stuck_out_tongue_closed_eyes:")} '
        ))
        await bot.send_message(chat_id=admin, text=md.text(md.text(f'Someone unknown tried to testify'),
                                                                md.text(f'Name:',
                                                                        md.code(callback_query.from_user.full_name)),
                                                                md.text(f'Username:',
                                                                        md.code(callback_query.from_user.username)),
                                                                md.text(f'ID:', md.code(callback_query.from_user.id)),
                                                                md.text(f'language:', md.code(
                                                                    callback_query.from_user.language_code)),
                                                                sep='\n',
                                                                ), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state='*', commands='stop')
@dp.message_handler(Text(equals='стоп', ignore_case=True), state='*')
async def cancel_handler(msg: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Today is not the best day for that, is it??')


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Form.gas_num)
async def process_num_invalid(msg: types.Message):
    """
    If gas_num is invalid
    """
    return await msg.reply("There should only be numbers.\nSend me the numbers on the gas meter to the point.")


@dp.message_handler(state=Form.gas_num)
async def gaz_num(msg: types.Message, state: FSMContext):
    '''
    ask of gas money
    '''
    async with state.proxy() as data:
        data['gas_num'] = int(msg.text)
    await Form.next()
    await msg.reply("And now how much money is left with kopecks?")


@dp.message_handler(lambda msg: not is_number(msg.text), state=Form.gas_rub)
async def process_num_invalid(msg: types.Message):
    """
    If gas_rub is invalid
    """
    return await msg.reply("There should only be numbers.\nSend me how much money is left with kopecks through the "
                           "point.")


@dp.message_handler(state=Form.gas_rub)
async def gaz_rub(msg: types.Message, state: FSMContext):
    '''
    ask of water money
    '''
    async with state.proxy() as data:
        data['gas_rub'] = float(msg.text)
    await Form.next()
    await msg.reply('What are the numbers on the water meter to the point?')


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Form.water)
async def process_age_invalid(msg: types.Message):
    """
    If water is invalid
    """
    return await msg.reply("There should only be numbers.\nSend me the numbers on the water meter to the point.")


@dp.message_handler(state=Form.water)
async def water(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['water'] = int(msg.text)
    await Form.next()
    await msg.reply('Now electricity. What are the first numbers?')


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Form.el1)
async def process_age_invalid(msg: types.Message):
    """
    If el1 is invalid
    """
    return await msg.reply("There should only be numbers.\nSend me the first digits of the counter.")


@dp.message_handler(state=Form.el1)
async def el1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['el1'] = int(msg.text)
    await Form.next()
    await msg.reply('And the second?')


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Form.el2)
async def process_age_invalid(msg: types.Message):
    """
    If el2 is invalid
    """
    return await msg.reply("There should only be numbers.\nSend me the second digits of the counter.")


@dp.message_handler(state=Form.el2)
async def el1(msg: types.Message, state: FSMContext):
    '''
    checking answers
    '''
    async with state.proxy() as data:
        data['el2'] = int(msg.text)
    await msg.reply('Fine! Check the data:')
    await msg.answer(md.text(
        md.text('Gas:', md.bold(data['gas_num'])),
        md.text('At the same time, money remained:', md.bold(data['gas_rub'])),
        md.text('Water:', md.bold(data['water'])),
        md.text(f'Electricity: {md.bold(data["el1"])} и {md.bold(data["el2"])}'),
        sep='\n',
    ), parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'right', state=Form)
async def process_callback_right(callback_query: types.CallbackQuery, state: FSMContext):
    '''
    count and answer
    '''
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Let me think...')
    await bot.send_animation(chat_id=callback_query.from_user.id,
                             animation='CgACAgQAAxkBAAIBf17Tp__QtIgx9Gnt6D7-GmZ91zvTAAJXAgACXa_0UkZXutz9iXmBGQQ')
    await types.ChatActions.typing()
    async with state.proxy() as data:
        if callback_query.from_user.id == admin:
            #if you are an admin you can write down any month
            await bot.send_message(callback_query.from_user.id, 'Which month?')
            await AddForm.add_mouth.set()
        else:
            count = count_engine.CountResources(data=data)
            count.gas()
            if count.gas_cost <= 0: #If there was an advance payment for gas.
                await bot.send_message(callback_query.from_user.id, 'I see you put money on the gas meter'
                                                                    '\nhow many?')
                await AddForm.add_gas.set()
            else:
                count.run()
                await total_message(callback_query.from_user.id, count)
                await total_message(admin, count, callback_query.from_user.full_name)
                count.write_to_file()
                await state.finish()
                await bot.send_animation(chat_id=callback_query.from_user.id,
                                         animation='CgACAgQAAxkBAAPfXtOKQ3nWRgYykrpo5Xa9uror7-MAAiUCAAJH4ZxS3C5y7WtyPdIZBA')


@dp.message_handler(state=AddForm.add_mouth)
async def add_mouth(msg: types.Message, state: FSMContext):
    '''
    if you change mouth
    '''
    async with state.proxy() as data:
        data['mouth'] = msg.text
        count = count_engine.CountResources(data=data, m=data['mouth'])
        count.gas()
        if count.gas_cost <= 0: #If there was an advance payment for gas.
            await msg.answer('I see you put money on the gas meter.\nhow many?')
            await AddForm.add_gas.set()
        else:
            count.run()
            await total_message(admin, count)
            count.write_to_file()
            await state.finish()
            await bot.send_animation(chat_id=msg.chat.id,
                                     animation='CgACAgQAAxkBAAPfXtOKQ3nWRgYykrpo5Xa9uror7-MAAiUCAAJH4ZxS3C5y7WtyPdIZBA')


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=AddForm.add_gas)
async def process_age_invalid(msg: types.Message):
    """
    If add_gas is invalid
    """
    return await msg.reply("There should only be numbers.\nHow much money did you put on the counter?.")


@dp.message_handler(state=AddForm.add_gas)
async def add_gas(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.from_user.id == admin:
            count = count_engine.CountResources(data=data, m=data['mouth'])
        else:
            count = count_engine.CountResources(data=data)
        count.run()
        count.gas(int(msg.text))
        await total_message(msg.chat.id, count, int(msg.text))
        await total_message(admin, count, msg.from_user.full_name, int(msg.text))
        count.write_to_file()
        await state.finish()
        await bot.send_animation(chat_id=msg.chat.id,
                                 animation='CgACAgQAAxkBAAPfXtOKQ3nWRgYykrpo5Xa9uror7-MAAiUCAAJH4ZxS3C5y7WtyPdIZBA')

@dp.message_handler(commands='?')
async def total_message(id, count, name_sender = None, add_gas=0):
    '''
    last message
    '''
    if id == admin: #send message to admin
        await bot.send_message(id, f'{name_sender} sent data')
    await bot.send_message(id, md.text(
        md.text('Gas - ', md.bold(count.gas_cost)),
        md.text('Water - ', md.bold(count.water_cost)),
        md.text('Electricity - ', md.bold(count.el_cost)),
        md.bold(f'AMOUNT {count.mouth} for a month:'),
        md.code(round(count.tot + add_gas, 2)), sep='\n'
    ), parse_mode=ParseMode.MARKDOWN)
