import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types='text')  # Функция отвечает на любой текст
def start_message(message):
    bot.send_message(message.chat.id,
                     f"Привет <b>{message.from_user.first_name}</b>!👋\nЯ бот котрый напомнит тебе о твоих делах.\n"
                     f"Просто напиши мне что и когда тебе напомнить.", parse_mode='html')


if __name__ == '__main__':
    bot.polling(none_stop=True)
