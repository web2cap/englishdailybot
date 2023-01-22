from django.shortcuts import get_object_or_404

from .models import TgPage


def get_tg_page(command):
    """Get command description by command name.
    If desabled return blank str."""

    page = get_object_or_404(TgPage, command=command)
    if page.enabled:
        return page.text
    return
