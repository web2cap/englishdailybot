from django.db import models

from core.models import CreatedModel
from users.models import User


class Collection(CreatedModel):
    """Collection of word with property native or custom and public/privare access.
    Parse field is service, only for admin panel usage and parsing."""

    ACCESS_CHOICES = ((False, "Private"), (True, "Public"))

    name = models.CharField(
        "Collection name",
        max_length=256,
        null=False,
        blank=False,
    )

    name_translated = models.CharField(
        "Translated Collection name",
        max_length=256,
        null=True,
        blank=True,
        default=None,
    )

    description = models.TextField(
        "Collection description", blank=True, null=True, default=None
    )

    author = models.ForeignKey(
        User,
        verbose_name="Collection author",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="collection",
    )

    access = models.BooleanField(
        "Public access enabled",
        choices=ACCESS_CHOICES,
        default=True,
        blank=False,
        null=False,
    )

    native = models.BooleanField(
        "Native community collection",
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
        return self.collection_subscription.count()

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
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

    collection = models.ManyToManyField(
        Collection, verbose_name="collection", related_name="words"
    )

    audio_us = models.BinaryField("USA pronunciation", null=True, default=None)
    audio_uk = models.BinaryField("GB pronunciation", null=True, default=None)

    example = models.TextField(
        "Example of usage", blank=True, null=True, default=None
    )

    @property
    def collections_count(self):
        return self.collection.count()

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"
        ordering = ["en"]

    def __str__(self):
        return self.en


class Translation(CreatedModel):
    """Translations for words."""

    tr = models.CharField(
        "Translation",
        max_length=128,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Translation"
        verbose_name_plural = "Translations"
        ordering = ["tr"]

    def __str__(self):
        return self.tr


class WordTranslation(CreatedModel):
    """Links of Translations for words."""

    word = models.ForeignKey(
        Word,
        verbose_name="Word",
        related_name="translation",
        on_delete=models.CASCADE,
    )

    translation = models.ForeignKey(
        Translation,
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

    class Meta:
        verbose_name = "Word Translation"
        verbose_name_plural = "Word Translations"
        ordering = ["native", "word"]

    def __str__(self):
        return self.word.en


class CollectionSubscription(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="collection_subscription",
        verbose_name="Follower",
        null=False,
        blank=False,
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="collection_subscription",
        verbose_name="Collection",
        null=False,
        blank=False,
    )

    rate = models.PositiveIntegerField(
        "Daily rate", null=True, blank=False, default=None
    )

    class Meta:
        verbose_name = "Collection subscriplion"
        verbose_name_plural = "Collection subscriplions"
        ordering = ["user", "-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "collection"], name="unique_subscriplion"
            )
        ]

    def __str__(self):
        return f"{self.user} by {self.collection}"


class WordLearn(CreatedModel):
    """User log in learning words."""

    STEP_CHOICE = (
        (0, "Skip"),
        (1, "Read"),
        (2, "Option"),
        (3, "Write"),
        (4, "Pass"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="words_learn",
        verbose_name="Learner",
        null=False,
    )

    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="words_learn",
        verbose_name="Learned word",
        null=False,
    )

    step = models.IntegerField(
        "Step",
        choices=STEP_CHOICE,
        blank=False,
        null=False,
    )

    result = models.BooleanField(
        "Result",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Word learning log"
        verbose_name_plural = "Words learning log"
        ordering = ["created"]

    def __str__(self):
        return f"{self.user}\t{self.word}\t{self.step}\t{self.result}"
