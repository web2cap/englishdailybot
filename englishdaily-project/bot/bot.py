from django.conf import settings
from telebot import TeleBot

TELEGRAM_BOT_API_KEY = getattr(settings, "TELEGRAM_BOT_API_KEY", None)

bot = TeleBot(TELEGRAM_BOT_API_KEY)