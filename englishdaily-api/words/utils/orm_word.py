import logging

from words.models import (
    Collection,
    Word,
    Translation,
    WordTranslation,
)

# WORD LIST

# EXAMPLE FOR VIEW
# def get_word_lists_with_subscription(tg_user_id, native=True):
#     """Get lists of word lists with subscription."""
#
#     from django.db.models import Q
#     user = User.objects.get(tg_id=tg_user_id)
#     return (
#         WordList.objects.filter(native=native)
#         .annotate(has_subscription=Q(word_list_subscription__user=user))
#         .order_by("-has_subscription")
#     )
#


def get_word_collections_for_parse():
    return Collection.objects.filter(parse__isnull=False)


def clear_word_collection_parse_field(list):
    list.parse = None
    list.save()


def add_word_to_collection(word, collection):
    if not word.collection.filter(id=collection.id).exists():
        word.collection.add(collection)
    logging.debug(f"WORD LISTS {word.collection}")


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
