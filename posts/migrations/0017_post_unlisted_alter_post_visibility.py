# Generated by Django 4.1.6 on 2023-04-02 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_post_is_github'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('FRIENDS', 'Friends')], default='PUBLIC', max_length=20),
        ),
    ]