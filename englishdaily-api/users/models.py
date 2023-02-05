from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        null=True,
    )

    last_name = models.CharField(
        "last name", max_length=150, blank=True, null=True
    )

    tg_id = models.BigIntegerField(
        verbose_name="Telegram id", unique=True, blank=False, null=False
    )

    language_code = models.CharField(
        max_length=4,
        verbose_name="Language code",
        blank=False,
        null=True,
        default=None,
    )

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Adding date and time"
    )

    REQUIRED_FIELDS = ["tg_id"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        return self.username
