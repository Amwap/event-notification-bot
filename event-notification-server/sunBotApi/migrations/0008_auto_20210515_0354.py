# Generated by Django 3.2.2 on 2021-05-15 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0007_auto_20210515_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='members',
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.TextField(blank=True, default='', verbose_name='Участники:'),
        ),
    ]