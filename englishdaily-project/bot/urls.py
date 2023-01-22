from django.urls import path
from django.conf import settings

from .views import index, dict_site


TELEGRAM_BOT_URL = getattr(settings, "TELEGRAM_BOT_URL", None)

app_name = "bot"

urlpatterns = [
    path(TELEGRAM_BOT_URL, index.as_view(), name="index"),
    path("dict/", dict_site),
]
