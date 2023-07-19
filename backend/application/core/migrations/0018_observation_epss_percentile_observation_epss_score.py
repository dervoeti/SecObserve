# Generated by Django 4.2.3 on 2023-07-14 18:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_product_last_observation_change"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="epss_percentile",
            field=models.DecimalField(
                decimal_places=3,
                max_digits=6,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
        migrations.AddField(
            model_name="observation",
            name="epss_score",
            field=models.DecimalField(
                decimal_places=3,
                max_digits=6,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]