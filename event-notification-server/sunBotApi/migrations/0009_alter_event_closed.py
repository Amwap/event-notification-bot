# Generated by Django 3.2.2 on 2021-05-16 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0008_auto_20210515_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='closed',
            field=models.BooleanField(default=True, verbose_name='Приём заявок.'),
        ),
    ]