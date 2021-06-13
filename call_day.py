import requests
import json
import datetime

base_url = 'https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/afisha?expand=spheres'

week_next = datetime.date.today()+datetime.timedelta(days=1)
today = datetime.date.today()
filter = '&filter={">date_from":"'+f'{today.year}-{today.month}-{today.day}'+'", "<date_from":"'+f'{week_next.year}-{week_next.month}-{week_next.day}'+'"}'

per_page = '&per-page=100&page=1'

resp = requests.get(base_url+filter+per_page)

dct = json.loads(resp.text)

import pandas as pd

df = pd.DataFrame(dct['items'])
d_today = df.sample(n=1)

import telebot

with open('token.txt',"r") as f:
    API_TOKEN = f.readlines()[0][:-1]

bot = telebot.TeleBot(API_TOKEN)
message = 'Сегодня, не пропустите:\n'

def post(subdf,message):
    for i, row in subdf.iterrows():
        sphere = row["spheres"][0]['title']
        title = row["title"]
        link0 = f'https://www.mos.ru/afisha/event/{row["id"]}'
        link = f'https://ivents.com/Ivent/{row["id"]}'
        dt = f"{row['date_from']}"[10:-3]
        img = "https://www.mos.ru/"+row["image"]["small"]["src"]
        descr = row['text']
        import html2text
        descr = html2text.html2text(descr)
        message += f'{title}\n{sphere}\n{dt}\n {descr} {link0}\n'
        bot.send_message('@MoscowFreeEvent',descr, parse_mode="HTML")
    return message

message = post(d_today.reset_index(),message)

bot.send_message('@MoscowFreeEvent',message, parse_mode="HTML")

