import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup 
import os
#from flask import Flask, request


API_KEY='5659848773:AAE9rS1gsy4K-9kLo6rJVSXT8JQKvpxpEII'
url='https://masstamilan.dev'
chat_id=-762532735


#app=Flask(__name__)

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

def web_crawler(link):
    base_url='https://masstamilan.dev'
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
                    Audio_link=base_url+href_value
                    title_list.append(title)
                    Audiolink_list.append(Audio_link)
    linkd = {title_list[i]: Audiolink_list[i] for i in range(len(title_list))}
    choose(linkd)

def try_statement(movie): 
    try:
        url1=url+'/'+word_checker(movie)+'-songs'
        web_crawler(url1)
    except AttributeError:
        try:
            url1=url+'/'+word_checker(movie)+'-hindi-songs'
            web_crawler(url1)
        except:
            try:
                url1=url+'/'+word_checker(movie)+'-malayalam-song'
                web_crawler(url1)
            except:
                try:
                    url1=url+'/'+word_checker(movie)+'-telugu-songs'
                    web_crawler(url1)
                except AttributeError:
                    bot.send_message(chat_id,text="Check the spelling")


def choose(dict):
    buttons = []
    for key, value in dict.items():
        buttons.append(
        [InlineKeyboardButton(text = key, url = value )]
        )
    keyboard = InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id,text = 'Songs from the movie ', reply_markup = keyboard)


bot=telebot.TeleBot(API_KEY,parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat_id, 'Welcome !! Enter a movie name')

@bot.message_handler(func=try_statement)
def pass_state(movie):
    pass

#@app.route("/"+ API_KEY,methods=["POST"])
#def getMessage():
#    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#    return "!", 200

#@app.route('/setwebhook', methods=['GET','POST'])
#def set_webhook():
#    webhook_url='https://http://killerganesh3.pythonanywhere.com/'
#    s=bot.set_webhook(url='{}{}'.format(webhook_url,API_KEY))
    
#    if s:
#        return "webhook setup ok"
#    else:
#        return "webhook setup failed"

#@app.route('/')
#def index():
#    return " welcome to index page"
#
#if __name__ == "__main__":
#    app.run(threaded=True)
bot.infinity_polling()
