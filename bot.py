#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import asyncio

import aiogram
from telebot.types import Message

import config
import data_process
import instruments
import organizer

bot = aiogram.Bot(config.TOKEN)
dp = aiogram.Dispatcher(bot)

state = None
state_time = {}


def user_init(message: Message):  # Функция инициализирует пользователя и сохраняет id
    while True:
        data = data_process.load_information()
        user_id = str(message.from_user.id)
        if user_id not in data:
            data_process.update_information(user_id, [])
        break


@dp.message_handler(commands=['start'])  # Функция отвечает на команду 'start'
async def start_message(message):
    user_init(message)
    await bot.send_message(message.chat.id,
                           f"Привет <b>{message.from_user.first_name}</b>!👋\nЯ бот, который напомнит тебе о твоих делах.\n"
                           f"Напиши команду /help, чтобы увидеть доступные команды!", parse_mode='html')


@dp.message_handler(commands=['create_task'])  # Функция отвечает на команду 'create_task'
async def create_task(message):
    await bot.send_message(message.chat.id,
                           "Напишите время в формате HH:MM")
    global state
    state = 'create_task_1'


@dp.message_handler(commands=['remove_task'])  # Функция отвечает на команду 'remove_task'
async def remove_task(message):
    await show_tasks(message)
    await bot.send_message(message.chat.id, 'Напишите номер дела в списке для удаления, например "/удали_дело 2"')
    global state
    state = 'remove_task'


@dp.message_handler(commands=['show_tasks'])  # Функция отвечает на команду 'show_tasks'
async def show_tasks(message):
    user_id = message.from_user.id
    current_org = organizer.Organizer(user_id)
    text = current_org.show_tasks()
    await bot.send_message(message.chat.id, text)


@dp.message_handler(content_types=['text'])  # Ввод нового времени и дела
async def remove_task(message):
    user_id = message.from_user.id
    current_org = organizer.Organizer(user_id)
    global state
    global state_time
    if state == 'create_task_1':
        state_time[user_id] = message.text
        await bot.send_message(message.chat.id, 'Введите ваше событие')
        state = 'create_task_2'
    elif state == 'create_task_2':
        description = message.text
        current_org.create_task(state_time[user_id], description)
        await bot.send_message(message.chat.id, 'Я успешно добавил дело в список')
        await run_task(message, state_time[user_id], description)
    elif state == 'remove_task':
        time_index = message.text
        current_org.remove_task(int(time_index))
        await bot.send_message(message.chat.id, 'Я удалил дело')
        state = None


async def run_task(message, time, description):
    try:
        sec_left = instruments.get_sec_left(time)
    except TypeError:
        await bot.send_message(message.chat.id, 'Я тебя не понял. Напишите время в формате HH:MM.')
        return
    await asyncio.sleep(sec_left)
    await bot.send_message(message.chat.id, 'Напоминаю!\n' + description)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
