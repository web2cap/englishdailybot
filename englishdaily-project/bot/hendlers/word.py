import logging

from random import randint

from telebot import custom_filters
from telebot.types import CallbackQuery
from telebot.callback_data import CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

from bot.bot import bot
from bot.controller import get_tg_page
from bot.factories.wordlist_factory import wordlist_factory
from bot.keyboards.native_wordlists import products_keyboard
from bot.states.wordlist_follow import WordListFollowState
from words.controller import get_word_list


def wordlist_message(message):
    """Start wordlist message. Choose the list for practice."""

    text = get_tg_page("wordlist")
    bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=products_keyboard(),
    )


class WordlistCallbackFilter(AdvancedCustomFilter):
    key = "config"

    def check(self, call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


def wordlist_follow_callback(call: CallbackQuery):
    callback_data: dict = wordlist_factory.parse(callback_data=call.data)
    id = int(callback_data["id"])
    list = get_word_list(id)
    if list:
        # get random string from  good answers from tgpages
        callback_answer = get_tg_page("wordlist_follow_callback").split("\n")
        callback_answer = callback_answer[randint(0, len(callback_answer) - 1)]
        bot.answer_callback_query(
            callback_query_id=call.id, text=callback_answer, show_alert=False
        )

        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.id
        )

        text = (
            f"List containt: {list.words_count} words\n"
            f"How many words from this list do you want to learn per day?:"
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
        )
        bot.set_state(
            call.from_user.id,
            WordListFollowState.rate,
            call.message.chat.id,
        )
        with bot.retrieve_data(
            call.from_user.id, call.message.chat.id
        ) as data:
            data["wordlist_id"] = id
            data["wordlist_count"] = list.words_count
        bot.register_next_step_handler(msg, ready_follow_wordlist)
    else:
        text = "List is not exist"
        bot.delete_state(call.message.from_user.id, call.message.chat.id)
        bot.send_message(call.message.chat.id, text=text)


# result
def ready_follow_wordlist(message):
    try:
        rate = int(message.text.strip())
        if rate < 1:
            raise ValueError("Not positive!")
    except:
        # ask rate again
        text = (
            "Please input positive digit, for example: 10\n"
            "How many words from this list do you want to learn per day?:"
        )
        wrong_rate_choice(message, text)
    with bot.retrieve_data(
        message.from_user.id, message.chat.id
    ) as condition_data:
        pass

    # if value is in range
    if rate > condition_data["wordlist_count"]:
        text = (
            f"Maximum for this list is: {condition_data['wordlist_count']}\n"
            "How many words from this list do you want to learn per day?:"
        )
        wrong_rate_choice(message, text)
        return

    text = (
        "Ready, take a look:\n"
        f"ID: {condition_data['wordlist_id']}\n"
        f"RATE: {rate}\n"
    )
    bot.send_message(message.chat.id, text=text)
    bot.delete_state(message.from_user.id, message.chat.id)


def wrong_rate_choice(message, text):

    msg = bot.send_message(
        chat_id=message.chat.id,
        text=text,
    )
    bot.register_next_step_handler(msg, ready_follow_wordlist)


def register_hendlers_word():
    bot.add_custom_filter(WordlistCallbackFilter())
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.register_message_handler(wordlist_message, commands=["wordlist"])
    bot.register_callback_query_handler(
        wordlist_follow_callback, func=None, config=wordlist_factory.filter()
    )
