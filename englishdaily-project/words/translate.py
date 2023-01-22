import re
import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup

from core.translate import translator
from .models import Word, WordList

DICT_URL = "https://wooordhunt.ru"
DICT_PAHT = "/word/"


def translate_list_to_db():

    lists = WordList.objects.filter(parse__isnull=False)
    for list in lists:
        parse_list = [w.strip() for w in list.parse.split(sep="\n")]
        for en in parse_list:
            en = re.sub(r"[^A-z- ]", "", en).lower()
            try:
                # translation = translator.translate(en)

                # word, created = Word.objects.get_or_create(
                #     en=en, defaults={"native": translation}
                # )
                # word.list.add(list)
                word = en

                print(scrap_translator(word))

                print(f"OK {word}")
                return
            except Exception as err:
                print(f"ERROR EXC: [{err}] {en}")
                # continue
                return
        # list.parse = None
        list.save()


def scrap_translator(word):
    """Parse rtanslator and get all data about word.
    Return dict with all data."""

    url = DICT_URL + DICT_PAHT + word
    url = "http://localhost:8000/bot/dict/"

    result = dict()

    # page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    # translation
    result["translation"] = (
        soup.find("div", class_="t_inline_en").get_text().split(sep=", ")
    )

    # examples
    ex_block = (
        soup.find("h3", text="Примеры с переводом").find_next().find_all("p")
    )
    result["examples"] = "\n".join([example.text for example in ex_block])

    # mp3
    audio_us_url = soup.find("audio", id="audio_us").source["src"]
    result["audio_us"] = get_mp3_by_link(audio_us_url)
    audio_uk_url = soup.find("audio", id="audio_uk").source["src"]
    result["audio_uk"] = get_mp3_by_link(audio_uk_url)

    return result


def get_mp3_by_link(url):
    try:
        url = DICT_URL + url
        with urlopen(url) as file:
            content = file.read()
        return content
    except:
        return None
