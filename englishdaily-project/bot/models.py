from django.db import models

from core.models import CreatedModel


class TgPage(CreatedModel):

    command = models.CharField(
        "command",
        max_length=64,
        unique=True,
        help_text="Required. 64 characters or fewer. Letters, digits in lower case, without /.",
        null=False,
        blank=False,
    )

    text = models.TextField(
        "Message text",
        blank=True,
        null=True,
        default=None,
    )

    enabled = models.BooleanField(
        "Enabled",
        blank=False,
        null=False,
        default=True,
    )

    updated = models.DateTimeField(
        "Updated date",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Telegram page"
        verbose_name_plural = "Telegram pages"
        ordering = ["command"]

    def __str__(self):
        return self.command
