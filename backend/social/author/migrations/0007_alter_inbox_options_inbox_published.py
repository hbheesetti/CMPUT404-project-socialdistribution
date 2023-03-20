# Generated by Django 4.1.7 on 2023-03-17 18:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0006_rename_type_followrequest_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inbox',
            options={'ordering': ['published']},
        ),
        migrations.AddField(
            model_name='inbox',
            name='published',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]