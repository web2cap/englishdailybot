import logging

from .models import WordList, Word, Translation, WordTranslation


def get_word_lists(native=True, user_rg_id=None):
    """Get lists of word lists."""
    list = WordList.objects.filter(native=native).all()
    if list.exists():
        return list
    return []


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


def add_word_to_list(word, list):
    if not word.list.filter(id=list.id).exists():
        word.list.add(list)
    logging.debug(f"WORD LISTS {word.list}")


def word_exist(en):
    return Word.objects.filter(en=en).exists()
