import telebot

API_TOKEN = 'your_api_token'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome! This is a simple Telegram bot.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling()