# Generated by Django 3.2.2 on 2021-05-13 06:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('admin_id', models.CharField(max_length=50, verbose_name='Telegram ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название события')),
                ('text', models.TextField(blank=True, verbose_name='Текст события')),
                ('annonce', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('publish', models.BooleanField(default=False, verbose_name='Опубликовать')),
                ('ended', models.BooleanField(default=False, verbose_name='Завершено')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='ФИО студента')),
                ('ticket_code', models.CharField(max_length=50, verbose_name='Код студенческого билета')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('nco', models.BooleanField(default=False, verbose_name='НСО')),
                ('verified', models.CharField(default='Не верифицирован.', max_length=50, verbose_name='Верификация:')),
                ('reg_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата добавления')),
                ('deactivated', models.BooleanField(default=False, verbose_name='Отключить от рассылки')),
            ],
        ),
    ]