import re

from core.translate import translator
from .models import Word, WordList


def translate_list_to_db():

    lists = WordList.objects.filter(parse__isnull=False)
    for list in lists:
        parse_list = [w.strip() for w in list.parse.split(sep="\n")]
        for en in parse_list:
            en = re.sub(r"[^A-z- ]", "", en).lower()
            try:
                translation = translator.translate(en)
                if translation:
                    word, created = Word.objects.get_or_create(
                        en=en, defaults={"native": translation}
                    )
                    word.list.add(list)
                    print(f"OK {word}")
            except:
                print(f"Err {en}")
                continue
        list.parse = None
        list.save()
