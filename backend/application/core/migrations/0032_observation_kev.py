# Generated by Django 4.2.10 on 2024-02-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0031_observation_issue_tracker_issue_closed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="kev",
            field=models.BooleanField(default=False),
        ),
    ]
