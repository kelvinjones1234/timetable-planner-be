# Generated by Django 5.0 on 2024-08-30 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("plan_app", "0003_examtimetableplan_course_set_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="examtimetableplan",
            old_name="course_set",
            new_name="course_set_name",
        ),
        migrations.RenameField(
            model_name="examtimetableplan",
            old_name="venue_set",
            new_name="venue_set_name",
        ),
    ]
