
import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get API tokens from environment variables or config.py
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# If tokens are not found in environment, try to import from config.py
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    try:
        from config import TELEGRAM_BOT_TOKEN as CFG_TELEGRAM_BOT_TOKEN, OPENAI_API_KEY as CFG_OPENAI_API_KEY
        if not TELEGRAM_BOT_TOKEN: TELEGRAM_BOT_TOKEN = CFG_TELEGRAM_BOT_TOKEN
        if not OPENAI_API_KEY: OPENAI_API_KEY = CFG_OPENAI_API_KEY
    except ImportError:
        pass

# Validate that tokens are available
if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN':
    print("Error: TELEGRAM_BOT_TOKEN is not set.")
if not OPENAI_API_KEY or OPENAI_API_KEY == 'YOUR_OPENAI_API_KEY':
    print("Error: OPENAI_API_KEY is not set.")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != 'YOUR_TELEGRAM_BOT_TOKEN' else None
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and OPENAI_API_KEY != 'YOUR_OPENAI_API_KEY' else None

# Store conversation history for each user
conversation_history = {}

async def get_openai_response(user_id: int, prompt: str):
    global conversation_history
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Add user's message to history
    conversation_history[user_id].append({"role": "user", "content": prompt})

    # Keep history to a reasonable length (e.g., last 10 messages)
    if len(conversation_history[user_id]) > 10:
        conversation_history[user_id] = conversation_history[user_id][-10:]

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. You can answer questions, provide information, and assist with various tasks. Be concise and helpful."}
    ] + conversation_history[user_id]

    try:
        if not client:
            return "OpenAI client is not initialized. Please check your API key."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        ai_response = response.choices[0].message.content
        # Add AI's response to history
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        logging.error(f"Error getting OpenAI response: {e}")
        return f"I'm sorry, I couldn't process your request: {str(e)}"

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm your AI assistant. How can I help you today?")

@dp.message()
async def handle_message(message: types.Message):
    if message.text:
        user_id = message.from_user.id
        logging.info(f"User {user_id} sent message: {message.text}")
        response_text = await get_openai_response(user_id, message.text)
        await message.reply(response_text)
    else:
        await message.reply("I can only process text messages for now.")

async def main():
    if not bot:
        logging.error("Bot token is missing. Exiting.")
        return
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
