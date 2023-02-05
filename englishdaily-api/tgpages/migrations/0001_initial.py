# Generated by Django 4.1.5 on 2023-02-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TgPage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="date of creation",
                    ),
                ),
                (
                    "command",
                    models.CharField(
                        help_text="Required. 64 characters or fewer. Letters, digits in lower case, without /.",
                        max_length=64,
                        unique=True,
                        verbose_name="command",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, default=None, null=True, verbose_name="Message text"
                    ),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="Enabled")),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated date"),
                ),
            ],
            options={
                "verbose_name": "Telegram page",
                "verbose_name_plural": "Telegram pages",
                "ordering": ["command"],
            },
        ),
    ]