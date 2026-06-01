import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Binance
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    
    # Discord
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
    DISCORD_ENABLED = os.getenv('DISCORD_ENABLED', 'true').lower() == 'true'
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'true').lower() == 'true'
    
    # Desktop Notifications
    DESKTOP_NOTIFICATIONS_ENABLED = os.getenv('DESKTOP_NOTIFICATIONS_ENABLED', 'true').lower() == 'true'
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Bot Settings
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))
    EMA_SHORT_PERIOD = int(os.getenv('EMA_SHORT_PERIOD', '8'))
    EMA_LONG_PERIOD = int(os.getenv('EMA_LONG_PERIOD', '21'))
