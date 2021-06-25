from django.db import models
from django.utils import timezone


class User(models.Model):
    ticket_code = models.CharField('Код студенческого билета', max_length=50, unique=True)
    email = models.CharField('Email', max_length=50)
    nco = models.BooleanField('НСО', default=False)
    verified = models.CharField('Верификация:', max_length=50, default='Не верифицирован.')
    reg_date = models.DateTimeField('Дата добавления', default=timezone.now)
    note = models.TextField('Для примечаний:', blank=True, default='')
    events = models.TextField('Мероприятия:', blank=True, default='')
    deactivated = models.BooleanField('Отключить от рассылки', default=False)

    def full_name(self):
        return f'{self.ticket_code}'

    def __str__(self): 
        text = ''
        if self.verified != 'Не верифицирован.':
            text = '- Верифицирован'
        return f"{self.full_name()} {text}"


class Event(models.Model):
    title = models.CharField('Название события', max_length=50)
    text = models.TextField('Текст события', blank=True)
    nco = models.BooleanField('Для НСО', default=True)
    annonce = models.DateTimeField('Дата создания', default=timezone.now)
    members = models.TextField('Участники:', blank=True, default='')
    publishing = models.BooleanField('Публиковать', default=False)
    closed = models.BooleanField('Приём заявок.', default=True)
    note = models.TextField('Для примечаний:', blank=True, default='')


    def __str__(self): 
        status = ''
        closed = ''
        if self.publishing == True:
            status = '- Публикуется'
            if self.closed == False:
                closed = '- Закрыто'

        return f"{self.title} {status} {closed}"


class Admin(models.Model):
    name = models.CharField('Имя', max_length=50)
    admin_id = models.CharField('Telegram ID', max_length=50)

    def __str__(self): 
        return f"{self.name} - {self.admin_id}"
