# Generated by Django 4.1.7 on 2023-03-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0008_author_github'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='github',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
    ]
