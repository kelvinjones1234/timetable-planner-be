# Generated by Django 5.0 on 2024-08-30 17:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="examtimetableplan",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
