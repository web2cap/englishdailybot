from telebot.handler_backends import State, StatesGroup


class WordListFollowState(StatesGroup):
    wordlist_id = State()
    rate = State()
