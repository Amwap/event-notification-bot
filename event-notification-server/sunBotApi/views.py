from typing import Text
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from .models import *
from sunProjectServer.settings import API_ACCESS
import json
import datetime

class Gateway(View):
    def get(self, request):
        if request.GET['key'] != API_ACCESS:
            return

        if request.GET['type'] == 'getmailing':
            """ /request?key={access_key}&type=getmailing 
                Возвращает список id для рассылки
            """

            id_list = User.objects.filter(deactivated=False).exclude(verified='Не верифицирован.').exclude(nco=False)
            data = [i.verified for i in id_list]
            return HttpResponse(json.dumps(data, ensure_ascii=True))

        elif request.GET['type'] == 'getadmin':
            """ /request?key={access_key}&type=getadmin 
                Возвращает список id для рассылки
            """
            data = Admin.objects.all()
            admins = [i.admin_id for i in data]
            return HttpResponse(json.dumps(admins, ensure_ascii=True))

        elif request.GET['type'] == 'getarticles':  # Получение списка доступных событий
            """ /request?key={access_key}&type=getarticles 
                Возвращает массив доступных событий
            """
            articles = Event.objects.filter(publishing=True)
            data = []
            for i in articles:
                data.append({
                    'id': i.id, 
                    'title': i.title, 
                    'text': i.text, 
                    'nco': i.nco
                })

            return HttpResponse(json.dumps(data, ensure_ascii=True))


        elif request.GET['type'] == 'getevent':  # Получение списка доступных событий
            """ /request?key={access_key}&type=getevent&eventId=
                Возвращает ивент или не существует
            """
            event_id = request.GET['eventId']
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return HttpResponse(json.dumps(['event not exist'], ensure_ascii=True))

            data = {
                'id': event.id,
                'title': event.title, 
                'text': event.text, 
                'register': event.closed,
                'members': event.members,
                'nco': event.nco,
                'closed': event.closed,
            }
            return HttpResponse(json.dumps(data, ensure_ascii=True))


        elif request.GET['type'] == 'getuser':
            """ /request?key={access_key}&type=getuser&tgId=
                Возвращает данные пользователя 
            """
            tg_id = str(request.GET['tgId'])
            try: 
                data = User.objects.get(verified=tg_id)
                user = {
                    'id': data.id,
                    'name': data.full_name(), 
                    'code': data.ticket_code,
                    'email': data.email,
                    'nco': data.nco,
                    'deactivated': data.deactivated
                }
            except User.DoesNotExist: user = None
            return HttpResponse(json.dumps(user, ensure_ascii=True))
        
        elif request.GET['type'] == 'getuserbyticket':
            """ /request?key={access_key}&type=getuserbyticket&ticket=
                Возвращает данные пользователя
            """
            ticket = str(request.GET['ticket'])
            try: 
                data = User.objects.get(ticket_code=ticket)
                user = {
                    'id': data.id,
                    'name': data.full_name,
                    'code': data.ticket_code,
                    'email': data.email,
                    'nco': data.nco,
                    'deactivated': data.deactivated
                }
            except User.DoesNotExist: user = None
            
            return HttpResponse(json.dumps(user, ensure_ascii=True))

        # elif request.GET['type'] == 'getusername':
        #     """ /request?key={access_key}&type=getusername&ticket=
        #         Возвращает имя пользователя
        #     """
        #     ticket = str(request.GET['ticket'])
        #     try: 
        #         data = User.objects.get(ticket_code=ticket)
        #         user = [data.name]
        #     except User.DoesNotExist: user = None
        #     return HttpResponse(json.dumps(user, ensure_ascii=True))


        elif request.GET['type'] == 'verify':  # запрос верификации
            """ /request?key={access_key}&type=verify&ticket=&tgId=&addnco=
                Возвращает код верификации или False
            """
            tg_id = request.GET['tgId']
            ticket = str(request.GET['ticket'])
            addnco = str(request.GET['addnco'])
            
            try: 
                user = User.objects.get(ticket_code=ticket)
                if addnco == '1':
                    user.nco = True
                if user.nco == False: 
                    user.verified = tg_id
                    user.save()
                    resp = [['verify complete', user.email]]

                elif user.nco == True: 
                    user.verified = tg_id
                    user.save()
                    resp = [['verify complete']]

            except User.DoesNotExist: resp = [['user not found']]
            return HttpResponse(json.dumps(resp, ensure_ascii=True))


        elif request.GET['type'] == 'acceptevent':
            """ /request?key={access_key}&type=acceptevent&event_id=&user_id= 
                Регистрирует участников на ивент
            """

            event_id = request.GET['event_id']
            user_id = request.GET['user_id']
            
            event = Event.objects.get(id=event_id)
            if event.closed == True: 
                user = User.objects.get(verified=user_id)
                user.events += f'\n{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")} {event.title}'
                text = f'{event.members}\n{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")} {user.full_name()}'
                event.members = text
                user.save()
                event.save()
                return HttpResponse(json.dumps(['succesfull'], ensure_ascii=True))

            else: return HttpResponse(json.dumps(['closed'], ensure_ascii=True))

        elif request.GET['type'] == 'checkticket':
            """ /request?key={access_key}&type=checkticket&ticket=
                Проверяет зарегистрирован пользователь или нет
            """
            ticket = str(request.GET['ticket'])
            try: 
                user = User.objects.get(ticket_code=ticket)
                if user.verified != "Не верифицирован.":
                    data = True
                else: data = False
            except User.DoesNotExist: data = None
            return HttpResponse(json.dumps(data, ensure_ascii=True))

        
        elif request.GET['type'] == 'getemailbyticket':
            """ /request?key={access_key}&type=getemailbyticket&ticket=
                Возвращает email по тикету или тщту
            """
            ticket = str(request.GET['ticket'])
            try: 
                user = User.objects.get(ticket_code=ticket)
                data = user.email
            except User.DoesNotExist: data = None
            return HttpResponse(json.dumps(data, ensure_ascii=True))