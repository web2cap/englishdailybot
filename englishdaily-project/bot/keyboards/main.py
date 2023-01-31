from telebot.types import ReplyKeyboardMarkup


kb_main = ReplyKeyboardMarkup(True)
kb_main.row("/start", "/help")
kb_main.row("/wordlist", "/learn")
