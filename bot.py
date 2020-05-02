#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import telebot
from telebot.types import Message

import config
import data_process
import organizer

bot = telebot.TeleBot(config.TOKEN)


def user_init(message: Message):  # Функция инициализирует пользователя и сохраняет его id
    while True:
        data = data_process.load_information()
        user_id = message.from_user.id
        if user_id not in data:
            data_process.update_information(user_id, [])
        break


@bot.message_handler(commands=['start'])  # Функция отвечает на команду 'start'
def start_message(message):
    user_init(message)
    bot.send_message(message.chat.id,
                     f"Привет <b>{message.from_user.first_name}</b>!👋\nЯ бот котрый напомнит тебе о твоих делах.\n"
                     f"Просто напиши мне что и когда тебе напомнить.", parse_mode='html')


@bot.message_handler(commands=['create_task'])  # Функция отвечает на команду 'start'
def create_task(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id,
                     "Напишите время в формате HH:MM и текст события. Например: '22:15>Бла-бла-бла'")
    time, description = message.text.split('>')
    current_org = organizer.Organizer(user_id)
    current_org.create_task(time, description)


@bot.message_handler(commands=['remove_task'])  # Функция отвечает на команду 'start'
def remove_task(message):
    user_id = message.from_user.id
    current_org = organizer.Organizer(user_id)
    show_tasks(message)
    bot.send_message(message.chat.id, 'Напишите номер дела в списке для удаления, например "/удали_дело 2"')
    current_org.remove_task(message.text)


@bot.message_handler(commands=['show_tasks'])  # Функция отвечает на команду 'start'
def show_tasks(message):
    user_id = message.from_user.id
    current_org = organizer.Organizer(user_id)
    text = current_org.show_tasks()
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
