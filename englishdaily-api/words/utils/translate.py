import logging
import re
import time

from random import randint

from words.utils.translate import translator
from words.utils.parse_dict import scrap_translator
from words.utils.orm_word import (
    add_word,
    add_word_to_collection,
    get_word_collections_for_parse,
    clear_word_collection_parse_field,
    word_exist,
)


def translate_list_to_db():
    lists = get_word_collections_for_parse()
    for list in lists:
        parse_list = [w.strip() for w in list.parse.split(sep="\n")]
        for en in parse_list:
            en = re.sub(r"[^A-z- ]", "", en).lower()
            if en and not word_exist(en):
                try:
                    word = scrap_translator(en)
                    if (
                        not word
                        or not word["translation"]
                        or not len(word["translation"])
                    ):
                        word = {}
                        logging.warning(f"No dict for {en}, trying google")
                        word["translation"] = [
                            translator.translate(en).lower()
                        ]
                    word["en"] = en
                    word_instance = add_word(word)
                    if word_instance:
                        add_word_to_collection(word_instance, list)
                except Exception as err:
                    logging.error(f"ERROR TRANSLATE: [{err}] {en}")
                # sleep rand sec
                time.sleep(randint(0, 7))
        clear_word_collection_parse_field(list)
