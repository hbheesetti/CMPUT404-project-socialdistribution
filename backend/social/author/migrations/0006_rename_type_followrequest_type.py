# Generated by Django 4.1.7 on 2023-03-17 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_alter_author_options_followrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followrequest',
            old_name='Type',
            new_name='type',
        ),
    ]
