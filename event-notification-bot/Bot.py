#coding: utf-8
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import json
import requests
import threading
import time
import smtplib
from credentials import *
import random
# import subprocess
import datetime


bot = telebot.TeleBot(TOKEN)
admin = [1471099925]

TEST = True
RUN = True  # чекер статей


def j_open(name):
    with open(name, mode="r",encoding='utf8') as json_file:
        return json.load(json_file)

def j_save(name, var):
    with open(name, 'w', encoding='utf8') as json_file:
        json.dump(var, json_file, ensure_ascii=False)


# state = j_open('state.json')
available_events = j_open('availableEvents.json')
new_events = []


print(repr(available_events))

class State():
    def __init__(self) -> None:
        self.state_file = 'state.json'
        self.state = j_open(self.state_file)

    def __saveState(self):
        j_save(self.state_file, self.state)

    def dropState(self, call):
        self.state[str(call.from_user.id)] = {"state": '', "data":[]}
        self.__saveState()

    def setState(self, call, msg):
        """ Работа с состояниями """
        try: self.state[str(call.from_user.id)]['state'] = msg
        except: self.dropState(call)
        self.__saveState()

    def getState(self, call):
        try:
            return self.state[str(call.from_user.id)]['state']
        except:
            self.dropState(call)
            return self.state[str(call.from_user.id)]['state']


    def setData(self, call, data):
        self.state[str(call.from_user.id)]['data'] = data
        self.__saveState()

    def getData(self, call):
        return self.state[str(call.from_user.id)]['data']

    def updateData(self, call, item):
        self.state[str(call.from_user.id)]['data'].append(item)
        self.__saveState()

state = State()

def admin_auth(func):
    """ права администратора """
    def wrapper(message):
        admins = request_(f'{server}/request?key={access_key}&type=getadmin')
        if admins != 'request error': 
            if str(message.chat.id) in admins:
                return func(message)
    return wrapper


@bot.message_handler(commands=['myid'])
def welcome_start(message):
    """ Возвращает id пользователя телеграм """
    bot.send_message(message.from_user.id, message.from_user.id)

@bot.message_handler(commands=['help'])
def help_func(message):
    """ Возвращает id пользователя телеграм """
    text = """
*Основные команды:*    
/events - список актуальных мероприятий

Нашли ошибку?
/report <Описание ошибки>
    
"""
    bot.send_message(message.from_user.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['report'])
def welcome_start(message):
    bot.send_message(admin[0], message.text)



@bot.message_handler(commands=['say'])
@admin_auth
def say(message):
    print(message.text)
    text = message.text.replace('/say ', '')
    id_list = request_(f'{server}/request?key={access_key}&type=getmailing')

    for i in id_list:
        try: bot.send_message(i, text)
        except: pass

    

def request_(url):
    """ Обработка реквестов """
    try: 
        return json.loads(requests.get(url).content.decode("utf-8"))
    except:
        print(f'{datetime.datetime.now()} Не удалось выполнить запрос: {url}')
        return 'request error'

def sendEvent(user_id, event):
    """ Отправляет ивент """
    user = request_(f'{server}/request?key={access_key}&type=getuser&tgId={user_id}')
    event = request_(f'{server}/request?key={access_key}&type=getevent&eventId={event["id"]}')
    
    nco = ''
    if event['nco'] == True: nco = "Доступ: Только участники НСО"
    else: nco = "Доступ: Для всех желающих"

    text = f"*{event['title']}*\n\n{event['text']}\n\n{nco}"
    keyboard = InlineKeyboardMarkup()
    
    if user['code'] in event['members']: keyboard.add(InlineKeyboardButton(text="Вы приняли участие ✅", callback_data="0"))
    elif event['closed'] == False: keyboard.add(InlineKeyboardButton(text="Регистрация закрыта ❌", callback_data="0"))
    else: keyboard.add(InlineKeyboardButton(text="Принять участие 📝", callback_data=f"accept {event['id']}"))
    try: bot.send_message(user_id, text, reply_markup=keyboard, parse_mode='Markdown')
    except: print("Не удалось отправить сообщение")


def sendEvents(user_id):
    """ Отправляет все ивенты """
    user = request_(f'{server}/request?key={access_key}&type=getuser&tgId={str(user_id)}')
    if user == 'request error': 
        bot.send_message(user_id, "Сервер временно не доступен.")
        return

    if user == None: return

    if user['deactivated'] == True:
        bot.send_message(user_id, "Вы отключены от рассылки.")
        return

    for i in available_events:
        sendEvent(user_id, i)


@bot.message_handler(commands=['events'])
def welcome_start(message):
    """ Выводит список событий """
    sendEvents(message.from_user.id)

# @bot.message_handler(commands=['myevents'])
# def welcome_start(message):
#     """ Выводит список событий  пользователя """
#     sendEvents(message.from_user.id)

def massMailing(event):
    """ Массовая рассылка ивента """
    id_list = request_(f'{server}/request?key={access_key}&type=getmailing')
    if id_list == 'request error': return
    for i in id_list:
        sendEvent(i, event)

def deleteMessages(call):
    data = state.getData(call)
    for i in data:
        try: bot.delete_message(call.from_user.id, i)
        except: print('Ошибка удаления')
    state.setData(call, [])
    

@bot.message_handler(commands=['start'])
def welcome_start(message):
    """ Обработка команды старт """
    user = request_(f'{server}/request?key={access_key}&type=getuser&tgId={str(message.from_user.id)}')
    if user == 'request error': 
        bot.send_message(message.from_user.id, "Сервер временно не доступен")
        return

    state.dropState(message)
    if user == None:
        bot.send_message(message.from_user.id, 'Для регистрации на мероприятия, отправьте номер вашего студенческого билета:')
        state.setState(message, 'verify waiting')

    else:
        state.dropState(message) 
        sendEvents(message.from_user.id)

def sendVerifyCode(email):
    """ Отправляет код верификации. Возвращает none или код"""
    try:
        code = random.randint(1000, 9999)
        to_email = email
        text = f'%s %s' % ('Your verification code', str(code))
        text = text.encode('ascii')

        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(username, password)
        smtpserver.sendmail(username, [to_email], text)
        return code

    except: return None

@bot.message_handler(content_types=['text'])
def send_text(message):
    """ Обработка текстового ввода """
    tgid = str(message.from_user.id)
    if state.getState(message) == 'verify waiting':
        ticket = message.text
        check = request_(f'{server}/request?key={access_key}&type=checkticket&ticket={ticket}')
        if check == True:
            email = request_(f'{server}/request?key={access_key}&type=getemailbyticket&ticket={ticket}')
            state.setState(message, f'waiting code {message.text} {email}')
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Получить код", callback_data="waiting code changetg"))
            keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="abort"))
            text = 'Пользователь с данным номером уже зарегистрирован.\n'
            text1 = 'Чтобы принимать рассылку на данный телеграм аккаунт, вам необходимо подтвердить ваш email'
            msg = bot.send_message(message.from_user.id, text=text+text1, reply_markup=keyboard)
            state.updateData(message, msg.id)
            return

        status = request_(f'{server}/request?key={access_key}&type=verify&ticket={ticket}&tgId={tgid}&addnco=0')[0]
        # name = request_(f'{server}/request?key={access_key}&type=getusername&ticket={ticket}')

        if status[0] == 'user not in nco': # ОТКЛЮЧЕНА НА СЕРВЕРЕ
            bot.send_message(message.from_user.id, f'Регистрация завершена. Теперь вам доступны мероприятия:')
            sendEvents(message.from_user.id)
            # name = request_(f'{server}/request?key={access_key}&type=getusername&ticket={ticket}')
            state.setState(message, f'waiting code {message.text} {status[1]}')
            text = f'В данный момент вы не являетесь участником научного сообщества.\n'
            text1 = 'Для участия, введите код который мы отправим на ваш email.'
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Получить код", callback_data="waiting code"))
            keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="abort"))
            msg = bot.send_message(message.from_user.id, text+text1, reply_markup=keyboard)
            state.updateData(message, msg.id)

        elif status[0] == 'verify complete':
            bot.send_message(message.from_user.id, f'Регистрация завершена. Теперь вам доступны мероприятия:')
            sendEvents(message.from_user.id)
        
        elif status[0] == 'user not found':
            text = "Данный номер отсутствует в базе данных. \nПопробуйте ещё раз или обратитесь в деканат."
            bot.send_message(message.from_user.id, text)

    elif state.getState(message).startswith('waiting code'):
        if state.getState(message).split(' ')[-1] == message.text:
            ticket = state.getState(message).split(' ')[2]
            # name = request_(f'{server}/request?key={access_key}&type=getusername&ticket={ticket}')

            status = request_(f'{server}/request?key={access_key}&type=verify&ticket={ticket}&tgId={tgid}&addnco=1')[0]
            bot.send_message(message.from_user.id, f'Регистрация завершена. Теперь вы вам доступны мероприятия:')
            sendEvents(message.from_user.id)
            state.dropState(message)

        else: bot.send_message(message.from_user.id, 'Не верный код. Попробуйте ещё раз.')


    elif state.getState(message).startswith('waiting code changetg'):
        if state.getState(message).split(' ')[-1] == message.text:
            ticket = state.getState(message).split(' ')[2]
            # name = request_(f'{server}/request?key={access_key}&type=getusername&ticket={ticket}')
            status = request_(f'{server}/request?key={access_key}&type=verify&ticket={ticket}&tgId={tgid}&addnco=0')[0]
            bot.send_message(message.from_user.id, f'Регистрация завершена. Теперь вы вам доступны мероприятия:')
            sendEvents(message.from_user.id)
            state.dropState(message)

        else: bot.send_message(message.from_user.id, 'Не верный код. Попробуйте ещё раз.')



@bot.callback_query_handler(func=lambda call: True)
def query_handler(callback):
    """ Обработка нажатия на кнопку """
    if callback.data.startswith('abort'):
        deleteMessages(callback)
        state.dropState(callback)

    elif callback.data.startswith('accept'):
        event_id = callback.data.split(' ')[-1]
        event = request_(f'{server}/request?key={access_key}&type=getevent&eventId={event_id}')
        
        if event == 'request error': 
            bot.send_message(callback.from_user.id, "Сервер временно недоступен")
            return


        if (event != None) and (event == 'event not exist') or (event['closed'] == False):
            bot.send_message(callback.from_user.id, "Регистрация на данное мероприятие была закрыта.")
            state.setState(callback, '')
            return

        user = request_(f'{server}/request?key={access_key}&type=getuser&tgId={callback.from_user.id}')
        if (user['nco'] == False) and (event['nco'] == True):
            user = request_(f'{server}/request?key={access_key}&type=getuser&tgId={callback.from_user.id}')
            state.setState(callback, f'waiting code {user["code"]} {user["email"]}')

            text = f'В данный момент вы не являетесь участником научного сообщества.\n'
            text1 = 'Чтобы принять участие, введите код который мы отправим на ваш email.'
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Получить код", callback_data="waiting code"))
            keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="abort"))
            msg = bot.send_message(callback.from_user.id, text+text1, reply_markup=keyboard)
            state.updateData(callback, msg.id)
            return

        text = f"Подтвердите желание участвовать в мероприятии \"{event['title']}\""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Подтвердить", callback_data="regme"))
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="abort"))
        msg = bot.send_message(callback.from_user.id, text, reply_markup=keyboard)
        state.updateData(callback, msg.id)
        state.setState(callback, f"waiting accept {event_id}")


    elif state.getState(callback).startswith('waiting accept') and callback.data == 'regme':
        deleteMessages(callback)
        user_id = callback.from_user.id
        event_id = state.getState(callback).split(' ')[-1]
        event = request_(f'{server}/request?key={access_key}&type=getevent&eventId={event_id}')
        data = request_(f'{server}/request?key={access_key}&type=acceptevent&event_id={event_id}&user_id={user_id}')
        bot.send_message(callback.from_user.id, f"Вы успешно подали заявку на событие \"{event['title']}\"")


    elif state.getState(callback).startswith('waiting code'):
        deleteMessages(callback)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Получить код", callback_data="waiting code"))
        msg = bot.send_message(callback.from_user.id, 'Ожидание ввода. Если код не пришёл, проверьте папку "спам" или повторите попытку', reply_markup=keyboard)
        state.updateData(callback, msg.id)

        
        stat = state.getState(callback)
        email = stat.split(' ')[3]
        code = sendVerifyCode(email)
        if code != None: state.setState(callback, f'{stat} {code}')   
        else: bot.send_message(callback.from_user.id, "Ошибка почтового сервиса. Код не был отправлен")



def runBot():
    # global RUN
    """ Старт пуллинга """
    # try: 
    bot.polling(none_stop=True) #запуск
    # except: RUN = False
    # finally: subprocess.Popen(['python3.9', 'Bot.py', '&'])



def runEventScheduler():
    """ Проверяет наличие новых событий и отправляет новые """
    global available_events
    while RUN:
        time.sleep(5)
        data = request_(f'{server}/request?key={access_key}&type=getarticles')
        if data == "request error": continue
        for i in data:
            if i not in available_events:
                massMailing(i)
        available_events = data
        j_save('availableEvents.json', available_events)
        


if __name__ == "__main__":
    if RUN == False:
        runBot()
    else:
        t1 = threading.Thread(target=runBot)
        t2 = threading.Thread(target=runEventScheduler)
        t1.start() 
        t2.start()


#  Корневые сообщения
#  Верификация не мемберов НСО
#  Участие в событии для юзеров в базе данных
#  Расширенные статсы
#  Исключения на реквесты
#  тест отключения рассылки пользователя
#  убрать кнопки регистрации для зарегистрированных участников
#  Общая рассылка
#  Команда хелп
#  кредсы
#  обращение по имени пользователя из бд
#  Добавление событий в пользовательский лист
# TODO Отправка писем через мыло
#  Ошибка с регистрацией на закрытые мероприятия
#  неиспользование events не верифицированными пользователями
#  верификация при вводе кода
#  подтверждение через email для участия в конкурсах
#  поиск по билету в админке
