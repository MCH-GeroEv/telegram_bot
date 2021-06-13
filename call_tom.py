import requests
import json
import datetime

base_url = 'https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/afisha?expand=spheres'

week_next = datetime.date.today()+datetime.timedelta(days=2)
today = datetime.date.today()+datetime.timedelta(days=1)
filter = '&filter={">date_from":"'+f'{today.year}-{today.month}-{today.day}'+'", "<date_from":"'+f'{week_next.year}-{week_next.month}-{week_next.day}'+'"}'

per_page = '&per-page=100&page=1'

resp = requests.get(base_url+filter+per_page)

dct = json.loads(resp.text)

import pandas as pd

df = pd.DataFrame(dct['items'])

d_paid = df[df['free']==0].sample(n=2)
d_free = df[df['free']==1].sample(n=2)

import telebot

with open('token.txt',"r") as f:
    API_TOKEN = f.readlines()[0][:-1]

bot = telebot.TeleBot(API_TOKEN)
message = 'Интересные события на завтра:\n\nБесплатные:\n'

def post(subdf,message):
    for i, row in subdf.iterrows():
        sphere = row["spheres"][0]['title']
        title = row["title"]
        link0 = f' https://www.mos.ru/afisha/event/{row["id"]}'
        link = f'https://ivents.com/Ivent/{row["id"]}'
        dt = f"{row['date_from']}"
        message += f'{i+1}. {title}, {sphere},{dt},{link0}\n'
    return message

message = post(d_free.reset_index(),message)
message +='\n\nПлатные:\n'
message = post(d_paid.reset_index(), message)

bot.send_message('@MoscowFreeEvent',message)#, parse_mode="HTML")


