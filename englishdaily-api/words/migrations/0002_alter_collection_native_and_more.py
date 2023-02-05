# Generated by Django 4.1.5 on 2023-02-05 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("words", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="native",
            field=models.BooleanField(
                default=False, verbose_name="Native community collection"
            ),
        ),
        migrations.AlterField(
            model_name="collectionsubscription",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collection_subscription",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Follower",
            ),
        ),
    ]
