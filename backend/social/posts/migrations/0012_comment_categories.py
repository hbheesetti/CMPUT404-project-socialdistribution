# Generated by Django 4.1.7 on 2023-03-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_alter_comment_options_alter_post_origin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='categories',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
