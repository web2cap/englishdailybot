from telebot.callback_data import CallbackData


factory_subscribe = CallbackData("wordlist_id", prefix="wordlist_subscribe")
factory_unsubscribe = CallbackData(
    "wordlist_id", prefix="wordlist_unsubscribe"
)
factory_view = CallbackData("wordlist_id", prefix="wordlist_view")
