# Generated by Django 3.2.2 on 2021-05-14 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0005_auto_20210515_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='Закрыть приём заявок'),
        ),
    ]
