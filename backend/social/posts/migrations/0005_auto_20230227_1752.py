# Generated by Django 3.1.6 on 2023-02-28 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230225_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='post',
            name='source',
        ),
    ]