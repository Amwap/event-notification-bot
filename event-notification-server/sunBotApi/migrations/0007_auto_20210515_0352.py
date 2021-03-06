# Generated by Django 3.2.2 on 2021-05-15 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0006_event_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Приём заявок.'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='members',
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(to='sunBotApi.User'),
        ),
    ]
