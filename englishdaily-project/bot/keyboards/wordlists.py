from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.factories.wordlist import (
    factory_subscribe,
    factory_unsubscribe,
    factory_view,
)


def kb_subscription_wordlist(word_list):
    if word_list.has_subscription:
        follow_botton = InlineKeyboardButton(
            text="Unsubscribe",
            callback_data=factory_unsubscribe.new(wordlist_id=word_list.id),
        )
    else:
        follow_botton = InlineKeyboardButton(
            text="Subscribe",
            callback_data=factory_subscribe.new(wordlist_id=word_list.id),
        )

    InlineKeyboardMarkup(
        keyboard=[
            # [follow_botton],
            [
                InlineKeyboardButton(
                    text="View",
                    callback_data=factory_view.new(wordlist_id=word_list.id),
                )
            ],
        ]
    )
