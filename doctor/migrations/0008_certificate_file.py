# Generated by Django 5.1.7 on 2025-04-09 07:47

import doctor.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctor", "0007_certificate"),
    ]

    operations = [
        migrations.AddField(
            model_name="certificate",
            name="file",
            field=models.FileField(
                default=True,
                upload_to="doctor/certificated",
                validators=[doctor.models.validate_pdf],
            ),
        ),
    ]
