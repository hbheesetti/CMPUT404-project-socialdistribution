# Generated by Django 4.1.7 on 2023-03-31 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0010_remove_followrequest_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inbox',
            options={'ordering': ['-published']},
        ),
    ]
