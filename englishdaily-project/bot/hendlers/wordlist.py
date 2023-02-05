from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import InlineKeyboardMarkup

from bot.bot import bot
from bot.controller import get_tg_page
from bot.keyboards.main import kb_main
from bot.keyboards.wordlists import kb_subscription_wordlist
from words.controller import (
    follow_word_list,
    get_word_lists_with_subscription,
)


def follow_wordlist_start(message):
    """Start follow wordlist message. Choose the list for practice."""

    word_lists = get_word_lists_with_subscription(
        message.from_user.id, native=True
    )
    for word_list in word_lists:
        print(f"NAME {word_list.name}")
        text = word_list.name

        keyboard = kb_subscription_wordlist(word_list)
        bot.send_message(
            message.chat.id,
            text=text,
            reply_markup=keyboard,
        )


def handle_subscribe_callback(bot, update):
    # do something when the subscribe button is pressed
    callback_query = update.callback_query
    # process the callback_query data to extract the word list ID
    # word_list_id = # extract the word list ID from callback_query.data
    # update the word_list_subscription model to reflect the subscription
    # ...
    bot.answer_callback_query(callback_query.id, text=callback_query.data)


# class WordlistCallbackFilter(AdvancedCustomFilter):
#     key = "config"
#
#     def check(self, call: CallbackQuery, config: CallbackDataFilter):
#         return config.check(query=call)


# def follow_wordlist_callback(call: CallbackQuery):
#     """Callback for wordlist choice. Register State. Ask daily rate."""
#
#     callback_data: dict = factory_wordlist.parse(callback_data=call.data)
#     id = int(callback_data["id"])
#     list = get_word_list(id)
#     if list:
#         # get random string from  good answers from tgpages
#         callback_answer = get_tg_page("wordlist_follow_callback").split("\n")
#         callback_answer = callback_answer[randint(0, len(callback_answer) - 1)]
#         bot.answer_callback_query(
#             callback_query_id=call.id, text=callback_answer, show_alert=False
#         )
#
#         bot.delete_message(
#             chat_id=call.message.chat.id, message_id=call.message.id
#         )
#
#         text = (
#             f"List containt: {list.words_count} words\n"
#             f"How many words from this list do you want to learn per day?:"
#         )
#         msg = bot.send_message(
#             chat_id=call.message.chat.id,
#             text=text,
#         )
#         bot.set_state(
#             call.from_user.id,
#             FollowWordlistState.rate,
#             call.message.chat.id,
#         )
#         with bot.retrieve_data(
#             call.from_user.id, call.message.chat.id
#         ) as data:
#             data["wordlist_id"] = id
#             data["wordlist_count"] = list.words_count
#         bot.register_next_step_handler(msg, follow_wordlist_rate)
#     else:
#         text = "List is not exist"
#         bot.delete_state(call.message.from_user.id, call.message.chat.id)
#         bot.send_message(call.message.chat.id, text=text)


# result
def follow_wordlist_rate(message):
    """Catch rate ansver for follow. Store follow to db."""

    # check rate to positive int
    try:
        rate = int(message.text.strip())
        if rate < 1:
            raise ValueError("Not positive!")
    except:
        text = (
            "Please input positive digit, for example: 10\n"
            "How many words from this list do you want to learn per day?:"
        )
        # ask rate again
        follow_wordlist_rate_ask_again(message, text)
    with bot.retrieve_data(
        message.from_user.id, message.chat.id
    ) as condition_data:
        pass

    # check that rate in max range
    if rate > condition_data["wordlist_count"]:
        text = (
            f"Maximum for this list is: {condition_data['wordlist_count']}\n"
            "How many words from this list do you want to learn per day?:"
        )
        follow_wordlist_rate_ask_again(message, text)
        return

    # save follow
    follow = follow_word_list(
        message.from_user.id, condition_data["wordlist_id"], rate
    )
    if follow:
        text = "Thanks for a subscription"
    else:
        text = "Error subscription"

    bot.send_message(message.chat.id, text=text, reply_markup=kb_main)
    bot.delete_state(message.from_user.id, message.chat.id)


def follow_wordlist_rate_ask_again(message, text):
    """Ask rate again and register current step as next."""

    msg = bot.send_message(
        chat_id=message.chat.id,
        text=text,
    )
    bot.register_next_step_handler(msg, follow_wordlist_rate)


def register_hendlers_wordlist():
    # bot.add_custom_filter(WordlistCallbackFilter())
    # bot.add_custom_filter(custom_filters.StateFilter(bot))
    # bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.register_message_handler(follow_wordlist_start, commands=["wordlist"])

    # bot.register_callback_query_handler(
    #     follow_wordlist_callback, func=None, config=factory_wordlist.filter()
    # )
    # bot.register_callback_query_handler(
    #     handle_subscribe_callback, pattern="subscribe_.*"
    # )
    # bot.register_callback_query_handler(handle_unsubscribe_callback, pattern='unsubscribe_.*')
    # bot.register_callback_query_handler(handle_view_callback, pattern='view_.*')
