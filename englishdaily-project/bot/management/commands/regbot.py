from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from bot.bot import bot


TELEGRAM_BOT_SERVER = getattr(settings, "TELEGRAM_BOT_SERVER", None)
TELEGRAM_BOT_URL = getattr(settings, "TELEGRAM_BOT_URL", None)


class Command(BaseCommand):
    help = "Register and unregister bot server URL on Telegram server."

    def add_arguments(self, parser: CommandParser) -> None:

        parser.add_argument(
            "--delete",
            action="store_true",
            help="Unregister bot server URL",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        if options["delete"]:
            if bot.remove_webhook():
                print("Bot was unregistred on TG server.")
            return

        url = f"https://{TELEGRAM_BOT_SERVER}/bot/{TELEGRAM_BOT_URL}"
        print(f"url {url}")
        if bot.set_webhook(url=url):
            print("Bot was registred on TG server.")
        return
