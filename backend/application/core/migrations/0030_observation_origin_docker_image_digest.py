# Generated by Django 4.2.9 on 2024-01-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0029_adjust_observation_hashes"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="origin_docker_image_digest",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]