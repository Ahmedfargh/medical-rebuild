# Generated by Django 5.1.7 on 2025-05-03 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_alter_doctorchat_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctorchat",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 3, 2, 29, 16, 655357)
            ),
        ),
        migrations.AlterField(
            model_name="doctorchatroom",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 3, 2, 29, 16, 655357)
            ),
        ),
    ]
