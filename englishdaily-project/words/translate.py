import logging
import re
import requests
import time

from random import randint
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.conf import settings

from core.translate import translator
from .controller import (
    add_word,
    add_word_to_list,
    get_word_lists_for_parse,
    clear_word_lists_parse_field,
    word_exist,
)


DICT_URL = getattr(settings, "DICT_URL")
DICT_PAHT = getattr(settings, "DICT_PAHT")


def translate_list_to_db():

    lists = get_word_lists_for_parse()
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
                        add_word_to_list(word_instance, list)
                except Exception as err:
                    logging.error(f"ERROR TRANSLATE: [{err}] {en}")
                # sleep rand sec
                time.sleep(randint(0, 7))
        clear_word_lists_parse_field(list)


def scrap_translator(word):
    """Parse rtanslator and get all data about word.
    Return dict with all data."""

    url = DICT_URL + DICT_PAHT + word

    result = dict()
    try:
        # page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        # translation
        result["translation"] = (
            soup.find("div", class_="t_inline_en").get_text().split(sep=", ")
        )

        # examples
        ex_block = (
            soup.find("h3", text="Примеры с переводом")
            .find_next()
            .find_all("p")
        )
        result["examples"] = "\n".join([example.text for example in ex_block])

        # mp3
        audio_us = soup.find("audio", id=re.compile("^audio_us.*"))
        if audio_us:
            audio_us_url = audio_us.source["src"]
            result["audio_us"] = get_mp3_by_link(audio_us_url)

        audio_uk = soup.find("audio", id=re.compile("^audio_uk.*"))
        if audio_uk:
            audio_uk_url = audio_uk.source["src"]
            result["audio_uk"] = get_mp3_by_link(audio_uk_url)

    except Exception as err:
        logging.error(f"ERROR SCRAP: [{err}] {word}")
        return
    return result


def get_mp3_by_link(url):
    if not url:
        return
    try:
        url = DICT_URL + url
        with urlopen(url) as file:
            content = file.read()
        return content
    except Exception as err:
        logging.error(f"ERROR GETMP3: [{url}] {err}")
        return None
