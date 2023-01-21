from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

import logging

from words.translate import translate_list_to_db


class Command(BaseCommand):
    help = "Parse words from tempory field."

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.ERROR)

        translate_list_to_db()
        return
