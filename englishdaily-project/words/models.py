from django.db import models

from core.models import CreatedModel
from users.models import User


class WordList(CreatedModel):
    """List of word with property native or custom and public/privare access.
    Parse field is service, only for admin panrl usage."""

    ACCESS_CHOICES = ((False, "Private"), (True, "Public"))

    name = models.CharField(
        "Word List name",
        max_length=256,
        null=False,
        blank=False,
    )

    name_translated = models.CharField(
        "Translated Word List name",
        max_length=256,
        null=True,
        blank=True,
        default=None,
    )

    description = models.TextField(
        "Word List description", blank=True, null=True, default=None
    )

    author = models.ForeignKey(
        User,
        verbose_name="Word List author",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="word_lists",
    )

    access = models.BooleanField(
        "Public access",
        choices=ACCESS_CHOICES,
        default=True,
        blank=False,
        null=False,
    )

    native = models.BooleanField(
        "Native community word list",
        blank=False,
        null=False,
        default=False,
    )

    parse = models.TextField(
        "Add many words.",
        blank=True,
        null=True,
        default=None,
        help_text="For a quick addition, add one word per line in English.",
    )

    @property
    def words_count(self):
        return self.words.count()

    @property
    def popularity(self):
        return self.word_list_subscriplion.count()

    class Meta:
        verbose_name = "Words list"
        verbose_name_plural = "Words lists"
        ordering = ["-native", "author", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "author"], name="unique_name_by_author"
            )
        ]

    def __str__(self):
        return self.name


class Word(CreatedModel):
    """Words model."""

    en = models.CharField(
        "English word",
        max_length=128,
        null=False,
        blank=False,
        unique=True,
    )

    list = models.ManyToManyField(
        WordList, verbose_name="Words list", related_name="words"
    )

    example = models.TextField(
        "Example of usage", blank=True, null=True, default=None
    )

    @property
    def lists_count(self):
        return self.list.count()

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"
        ordering = ["en"]

    def __str__(self):
        return self.en


class Tranclation(CreatedModel):
    """Translations for words."""

    tr = models.CharField(
        "Translation",
        max_length=128,
        blank=False,
        null=False,
    )

    native = models.BooleanField(
        blank=False,
        null=False,
        default=True,
    )


class WordTranslation(CreatedModel):
    """Links of Translations for words."""

    word = models.ForeignKey(
        Word,
        verbose_name="Word",
        related_name="translation",
        on_delete=models.CASCADE,
    )

    translation = models.ForeignKey(
        Tranclation,
        verbose_name="Translation",
        related_name="word",
        on_delete=models.CASCADE,
    )

    cost = models.PositiveIntegerField(
        "Ordering value",
        blank=False,
        null=False,
        default=0,
    )

    native = models.BooleanField(
        "Native translation", null=False, blank=False, default=True
    )

    author = models.ForeignKey(
        User,
        verbose_name="Author of translation",
        null=True,
        on_delete=models.SET_NULL,
    )


class WordListSubscriplion(CreatedModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="word_list_subscriplion",
        verbose_name="Follower",
        null=False,
        blank=False,
    )

    list = models.ForeignKey(
        WordList,
        on_delete=models.CASCADE,
        related_name="word_list_subscriplion",
        verbose_name="Word list",
        null=False,
        blank=False,
    )

    rate = models.PositiveIntegerField(
        "Daily rate", null=True, blank=False, default=None
    )

    class Meta:
        verbose_name = "Word-list subscriplion"
        verbose_name_plural = "Word-list subscriplions"
        ordering = ["user", "-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "list"], name="unique_subscriplion"
            )
        ]

    def __str__(self):
        return f"{self.user} by {self.list}"
