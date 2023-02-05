from translate import Translator

from django.conf import settings


TRANSLATOR_FROM = getattr(settings, "TRANSLATOR_FROM", "en")
TRANSLATOR_TO = getattr(settings, "TRANSLATOR_TO", "ru")

translator = Translator(to_lang=TRANSLATOR_TO, from_lang=TRANSLATOR_FROM)

# how to use module
# translation = translator.translate("done")
