# Generated by Django 5.1.7 on 2025-05-03 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0008_allowedto"),
    ]

    operations = [
        migrations.AddField(
            model_name="allowedto",
            name="patient_approved",
            field=models.BooleanField(default=False),
        ),
    ]
