# Generated by Django 3.2.2 on 2021-05-17 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0010_auto_20210517_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(default='', max_length=20, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='surename',
            field=models.CharField(default='', max_length=20, verbose_name='Фамилия'),
        ),
    ]
