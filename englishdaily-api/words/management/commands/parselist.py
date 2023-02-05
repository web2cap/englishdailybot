from django.core.management.base import BaseCommand


from words.utils.translate import translate_list_to_db


class Command(BaseCommand):
    help = "Parse words from tempory field."

    def handle(self, *args, **options):
        translate_list_to_db()
        return
