# Generated by Django 5.1.7 on 2025-03-27 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Captcha",
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
                ("email", models.EmailField(max_length=254)),
                ("captcha", models.CharField(max_length=4)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
