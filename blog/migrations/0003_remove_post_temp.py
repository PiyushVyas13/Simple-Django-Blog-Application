# Generated by Django 4.1.1 on 2023-01-09 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_temp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="temp",
        ),
    ]
