# Generated by Django 5.0 on 2024-10-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_app", "0005_examtimetableplan_constraints"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="level",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
