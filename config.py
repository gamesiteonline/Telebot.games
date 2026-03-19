import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8684161160:AAHSuajosH6V25ypAYK4i2VMC5AOJCgxV60')
CHAT_ID = os.getenv('CHAT_ID', '')

# API Configuration
RAWG_API_KEY = os.getenv('RAWG_API_KEY', '')  # Get from https://rawg.io/
IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID', '')
IGDB_ACCESS_TOKEN = os.getenv('IGDB_ACCESS_TOKEN', '')

# Database Configuration
DB_PATH = os.getenv('DB_PATH', 'games.db')
DB_BACKUP_PATH = os.getenv('DB_BACKUP_PATH', 'games_backup.db')

# API Limits
API_RATE_LIMIT = 5  # requests per second
MAX_GAMES_PER_REQUEST = 40  # RAWG API returns max 40 per page
TOTAL_GAMES_TARGET = 1000000  # Target 1 million games

# Telegram Bot Settings
RESULTS_PER_PAGE = 5  # Games shown per message
MAX_MESSAGE_LENGTH = 4096  # Telegram message limit

# Platforms to support
SUPPORTED_PLATFORMS = {
    'pc': 1,
    'playstation': 2,
    'xbox': 3,
    'nintendo': 4,
    'ios': 5,
    'android': 6,
    'macos': 7,
    'linux': 8
}

# Store Links (for legitimate platforms)
STORE_LINKS = {
    'steam': 'https://store.steampowered.com/search/?q={game_name}',
    'epic': 'https://www.epicgames.com/store/en-US/search?q={game_name}',
    'gog': 'https://www.gog.com/en/games?search={game_name}',
    'itch': 'https://itch.io/games/search?q={game_name}',
    'origin': 'https://www.origin.com/usa/en-us/store/browse?q={game_name}',
    'ubisoft': 'https://store.ubisoft.com/us/search?q={game_name}'
}