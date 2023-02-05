import logging

from django.db.models import Q

from users.models import User
from .models import (
    WordList,
    Word,
    Translation,
    WordTranslation,
    WordListSubscription,
    WordLearn,
)

# WORD LIST


def get_word_lists(native=True):
    """Get lists of word lists."""

    list = WordList.objects.filter(native=native).all()
    if list.exists():
        return list
    return []


def get_word_lists_with_subscription(tg_user_id, native=True):
    """Get lists of word lists with subscription."""

    user = User.objects.get(tg_id=tg_user_id)
    return (
        WordList.objects.filter(native=native)
        .annotate(has_subscription=Q(word_list_subscription__user=user))
        .order_by("-has_subscription")
    )


def get_word_list(id):
    """Get list by id."""

    list = WordList.objects.filter(id=id)
    if not list.exists():
        return
    return list.first()


def get_word_lists_for_parse():
    return WordList.objects.filter(parse__isnull=False)


def clear_word_lists_parse_field(list):
    list.parse = None
    list.save()


def add_word_to_list(word, list):
    if not word.list.filter(id=list.id).exists():
        word.list.add(list)
    logging.debug(f"WORD LISTS {word.list}")


# WORD


def add_word(word):
    """Add word and translation to db from dict."""

    # word
    word_instance, created = Word.objects.get_or_create(
        en=word["en"],
        defaults={
            "audio_us": word.get("audio_us"),
            "audio_uk": word.get("audio_uk"),
            "example": word.get("examples"),
        },
    )
    if created:
        logging.info(f"ADD WORD {word_instance}")
    else:
        logging.debug(f"GET WORD {word_instance}")

    # translation and link
    cost = 0
    for tr in word["translation"]:
        translation, created = Translation.objects.get_or_create(tr=tr)
        WordTranslation.objects.create(
            word=word_instance, translation=translation, cost=cost, native=True
        )
        cost += 10
        if created:
            logging.debug(f"ADD TR {translation}")
        else:
            logging.debug(f"GET TR {translation}")

    return word_instance


def word_exist(en):
    return Word.objects.filter(en=en).exists()


# WordListSubscriplion
def follow_word_list(user_tg_id, list_id, rate):
    """Follow user to wordlist."""

    try:
        user = User.objects.get(tg_id=user_tg_id)
        list = WordList.objects.get(id=list_id)
        follow, _ = WordListSubscription.objects.update_or_create(
            user=user,
            list=list,
            defaults={"rate": rate},
        )
        return follow
    except Exception as err:
        logging.warning(f"follow_word_list: [{err}]")
        return False


# LEARN WORDS


def learn_words_hello(user_tg_id):
    """Get data before start learn session."""

    try:
        return User.objects.get(tg_id=user_tg_id).word_list_subscriplion
    except Exception as err:
        logging.warning(f"GET USER SUBSCRIPRION: [{err}]")
        return False
