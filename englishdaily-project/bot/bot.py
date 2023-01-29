import logging

from django.conf import settings
from telebot import TeleBot
from telebot.storage import StateRedisStorage

TELEGRAM_BOT_API_KEY = getattr(settings, "TELEGRAM_BOT_API_KEY", None)
REDIS_HOST = getattr(settings, "REDIS_HOST", None)
REDIS_PORT = getattr(settings, "REDIS_PORT", None)
REDIS_DB = getattr(settings, "REDIS_DB", None)
REDIS_PASSWORD = getattr(settings, "REDIS_PASSWORD", None)
REDIS_PREFIX = getattr(settings, "REDIS_PREFIX", None)

state_storage = StateRedisStorage(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=None,
    prefix=REDIS_PREFIX,
)

bot = TeleBot(TELEGRAM_BOT_API_KEY, state_storage=state_storage)

logging.getLogger("TeleBot").setLevel(logging.DEBUG)
