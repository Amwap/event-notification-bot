# Generated by Django 3.2.2 on 2021-05-17 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunBotApi', '0009_alter_event_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='patronymic',
            field=models.CharField(default='', max_length=20, verbose_name='ФИО студента'),
        ),
        migrations.AddField(
            model_name='user',
            name='surename',
            field=models.CharField(default='', max_length=20, verbose_name='ФИО студента'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, verbose_name='ФИО студента'),
        ),
    ]