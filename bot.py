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
task_loop = {}


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


@dp.message_handler(commands=['help'])  # Функция отвечает на команду 'help'
async def start_message(message):
    await bot.send_message(message.chat.id,
                           f"Список доступных команд:\n"
                           f"/create - создать новое напоминание\n"
                           f"/remove - удалить напоминание\n"
                           f"/show - показать список всех напоминаний\n"
                           f"/help - вывести список доступных команд\n", parse_mode='html')


@dp.message_handler(commands=['create'])  # Функция отвечает на команду 'create'
async def create_task(message):
    await bot.send_message(message.chat.id,
                           "Напишите время в формате HH:MM")
    global state
    state = 'create_task_1'


@dp.message_handler(commands=['remove'])  # Функция отвечает на команду 'remove_task'
async def remove_task(message):
    await show_tasks(message)
    await bot.send_message(message.chat.id, 'Напишите номер дела в списке для удаления')
    global state
    state = 'remove_task'


@dp.message_handler(commands=['show'])  # Функция отвечает на команду 'show_tasks'
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
    global task_loop
    if state == 'create_task_1':
        state_time[user_id] = message.text
        await bot.send_message(message.chat.id, 'Введите текст напоминания')
        state = 'create_task_2'
    elif state == 'create_task_2':
        description = message.text
        current_org.create_task(state_time[user_id], description)
        await bot.send_message(message.chat.id, 'Напоминание успешно добавлено!')
        task = asyncio.create_task(run_task(message, state_time[user_id], description))
        if user_id in task_loop:
            old_info = task_loop.pop(user_id)
            task_loop.update({user_id: old_info.update({state_time[user_id]: task})})
        else:
            task_loop[user_id] = {state_time[user_id]: task}
        await task
    elif state == 'remove_task':
        time_index = message.text
        time = list(current_org.task_list[int(time_index)].items())[0][0]  # Don't touch this!
        current_org.remove_task(int(time_index))
        task_loop[user_id].pop(time).cancel()  # Stop async await sleep()
        await bot.send_message(message.chat.id, 'Напоминание успешно удалено!')
        state = None


async def run_task(message, time, description):
    try:
        sec_left = instruments.get_sec_left(time)
    except TypeError:
        await bot.send_message(message.chat.id, 'Я тебя не понял. Напишите время в формате HH:MM.')
        return
    await asyncio.sleep(sec_left)
    await bot.send_message(message.chat.id, 'Новое напоминание:\n' + description)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
