# Generated by Django 4.1.5 on 2023-01-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_created_user_language_code_user_tg_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="last name"
            ),
        ),
    ]
