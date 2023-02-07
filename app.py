import logging
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
from telegram import Update,Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher

logger = logging.getLogger(__name__)

API_KEY='5659848773:AAE7mT3MfzUwQ1B3TrQIVi6LkECWMb7rgSg'
url='https://masstamilan.dev'

bot=Bot(API_KEY)
dp=Dispatcher(bot,None)

app=Flask(__name__)

def start_handler(update,context):
    update.message.reply_text('Hello there! Send me any movie name')
    
def handle_message(update, context):
    text = str(update.message.text).lower()
    update.message.reply_text(text)

def word_checker(update):
    movie=update.message.text
    words_list=movie.split()
    temp_str=''
    
    if len(words_list)>1:
        for word in words_list:
            if word==words_list[0]:
                temp_str=temp_str+word
            else:
                temp_str=temp_str+'-'+word
    else:
        temp_str=temp_str+movie
        
    required_format_word=temp_str.lower()  
    return required_format_word


def web_crawler(link,update):
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
                    title_list.append(title[:-8:])
                    Audiolink_list.append(Audio_link)
    linkd = {title_list[i]: Audiolink_list[i] for i in range(len(title_list))}
    choose(update,link_dictionary=linkd)

def choose(update: Update,link_dictionary= dict):
    msg = update.effective_message
    keyb = []
    for key, value in link_dictionary.items():
        keyb.append(
        [InlineKeyboardButton(text = key, url = value )]
        )
    msg.reply_text(f"Song from {update.message.text} movie", reply_markup=InlineKeyboardMarkup(keyb))

def try_statement(update,context): 
    try:
        tamil=url+'/'+word_checker(update)+'-songs'
        web_crawler(tamil,update)
    except AttributeError:
        try:
            hindi=url+'/'+word_checker(update)+'-hindi-songs'
            web_crawler(hindi,update)
        except AttributeError:
            try:
                malayalam=url+'/'+word_checker(update)+'-malayalam-song'
                web_crawler(malayalam,update)
            except AttributeError:
                try:
                    telugu=url+'/'+word_checker(update)+'-telugu-songs'
                    web_crawler(telugu,update)
                except AttributeError:
                    update.message.reply_text('check the spelling')

def error(update, context):
    logger.error("Update '%s' caused error '%s'", update, update.error)

@app.route('/'+API_KEY,methods=['POST'])
def getMessage():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok messages recieved",200

@app.route('/')
def webhook():
    bot.delete_webhook()
    bot.set_webhook(url="https://songrequestbot.onrender.com/"+API_KEY)
    return "! web hook ",200


if __name__=="__main__":
    dp.add_handler(CommandHandler('start',start_handler))
    dp.add_handler(MessageHandler(Filters.text,try_statement))
    dp.add_error_handler(error)
    app.run(debug=True,threaded=True)
