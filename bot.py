import telebot
import json

# Initialize bot with token
bot = telebot.TeleBot("8684161160:AAHSuajosH6V25ypAYK4i2VMC5AOJCgxV60")

# Load games from database
with open('database.json') as f:
    games = json.load(f)

# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.username or 'Guest'
    welcome_message = f"Welcome {user_name} to Fahad | Gamesite Online!"
    bot.send_message(message.chat.id, welcome_message)
    show_platform_buttons(message)

# Show platform selection buttons
def show_platform_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    platforms = ['PC', 'PlayStation', 'Xbox', 'Nintendo', 'iOS', 'Android', 'APK', 'Web']
    for platform in platforms:
        markup.add(platform)
    bot.send_message(message.chat.id, "Select your platform:", reply_markup=markup)

# Handle platform selection
@bot.message_handler(func=lambda message: message.text in ['PC', 'PlayStation', 'Xbox', 'Nintendo', 'iOS', 'Android', 'APK', 'Web'])
def handle_platform_selection(message):
    selected_platform = message.text
    filtered_games = filter_games_by_platform(selected_platform)
    show_game_selection(filtered_games, message)

# Filter games by platform
def filter_games_by_platform(platform):
    return [game for game in games if game['platform'] == platform]

# Show game selection
def show_game_selection(filtered_games, message):
    for game in filtered_games:
        bot.send_message(message.chat.id, f"{game['title']} - {game['description']}", reply_markup=get_download_buttons(game))

# Generate download buttons
def get_download_buttons(game):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="Download", url=game['download_link'])
    markup.add(button)
    return markup

# User session management (to be implemented)
# Callback handlers for all interactions (to be implemented)
# Back navigation buttons (to be implemented)

# Start polling
bot.polling()