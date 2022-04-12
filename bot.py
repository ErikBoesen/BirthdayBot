import os
import requests
import mebots
import yalies
import datetime
import json


with open('config.json', 'r') as f:
    config = json.load(f)
bot = mebots.Bot('butteur_bot', config['mebots_token'])
yalies_api = yalies.API(config['yalies_api_key'])


def get_students():
    date = datetime.date.today()
    students = yalies_api.people(filters={'college_code': 'GH', 'birth_month': date.month, 'birth_day': date.day})
    return [student.first_name + ' ' + student.last_name for student in students]


def send(text, bot_id):
    url  = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)

students = get_students()
message = None
if students:
    message = 'Happy birthday to '
    if len(students) > 1:
        last = students.pop()
        message += ', '.join(students)
        message += ', & ' + last
    else:
        message += students[0]
    message += '!'

    bot_ids = [instance.id for instance in bot.instances()]
    for bot_id in bot_ids:
        send(message, bot_id)
