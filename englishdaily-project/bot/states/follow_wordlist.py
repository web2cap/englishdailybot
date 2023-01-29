from telebot.handler_backends import State, StatesGroup


class FollowWordlistState(StatesGroup):
    wordlist_id = State()
    rate = State()
