# Generated by Django 4.1.1 on 2023-01-09 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="temp",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
