import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup 
import os
from flask import Flask, request


# API_KEY=  os.environ.get('API_KEY')
API_KEY='5659848773:AAE7mT3MfzUwQ1B3TrQIVi6LkECWMb7rgSg'
WEBHOOK='https://songrequestbot.onrender.com'
# WEBHOOK= os.environ.get('webhook_url')

url='https://masstamilan.dev'

bot=telebot.TeleBot(API_KEY)

app=Flask(__name__)

def word_checker(movie):
    movie=movie.text
    x=movie.split()
    z=''
    if len(x)>1:
        for word in x:
            if word==x[0]:
                z=z+word
            else:
                z=z+'-'+word
    else:
        z=z+movie
    MOVIE=z.lower()      
    return MOVIE

def web_crawler(link,message):
    # base_url='https://masstamilan.dev'
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_list=[]
    Audiolink_list=[]
    for row in soup.find('tbody').find_all('tr'):
        col3=row.find_all('td')
        for links in col3:
            link=links.find_all('a')
            for content in link:
                href_value=content.get('href')
                title=content.get('title')
                b=str(content)
                val=b.split()
                if (title is not None and str(title)[:-8:-1]=='spbk023') and ('rel="nofollow"' in val): 
                    Audio_link=url+href_value
                    title_list.append(title)
                    Audiolink_list.append(Audio_link)
    linkd = {title_list[i]: Audiolink_list[i] for i in range(len(title_list))}
    choose(linkd,message)


def choose(dict,message):
    buttons = []
    for key, value in dict.items():
        buttons.append(
        [InlineKeyboardButton(text = key, url = value )]
        )
    keyboard = InlineKeyboardMarkup(buttons)
    bot.reply_to(message,text = f'🎧<b>{message.text}</b> movie songs🎧',parse_mode='HTML' ,reply_markup = keyboard)


bot=telebot.TeleBot(API_KEY,parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=f'Hi <b>{message.from_user.first_name}</b>👋👋👋 \nWelcome to the channel !! Enter a movie name',parse_mode='HTML')

@bot.message_handler(func= lambda msg: msg.content_type=='text')
def try_statement(movie):
    try:
        tamil=url+'/'+word_checker(movie)+'-songs'
        web_crawler(tamil,movie)
    except AttributeError:
        try:
            hindi=url+'/'+word_checker(movie)+'-hindi-songs'
            web_crawler(hindi,movie)
        except:
            try:
                malayalam=url+'/'+word_checker(movie)+'-malayalam-song'
                web_crawler(malayalam,movie)
            except:
                try:
                    telugu=url+'/'+word_checker(movie)+'-telugu-songs'
                    web_crawler(telugu,movie)
                except AttributeError:
                    bot.reply_to(movie,text="Check the spelling")

@app.route("/"+ API_KEY,methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/setwebhook', methods=['GET','POST'])
def set_webhook():
    s=bot.set_webhook(url='{}{}'.format(WEBHOOK,API_KEY))
    
    if s:
        return "<h1>    Webhook setup ok</h1>"
    else:
        return "<h1>    Webhook setup failed</h1>"

@app.route('/')
def index():
    return " welcome to index page"

if __name__ == "__main__":
    app.run(threaded=True)
