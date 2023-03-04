import os
import telebot
import openai
import dotenv
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

general_engine = "text-davinci-003"
code_engine = "code-davinci-002"
max_tokens = 1024
temperature = 0.2

chat_id = 442525356

def chooselanguage():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("English", callback_data="cb_english"),
    InlineKeyboardButton("Ukrainian", callback_data="cb_ukrainian"),)
    return markup

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, 'Hello! Please, choose your language.', reply_markup=chooselanguage())
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_english":
        bot.send_message(call.message.chat.id, 'Hello! Im ChatGPT telegram bot\n' 'Im using GPT-3.5 engine\n'
                     '\nFor general purpose questions please, select general mode, which using text-davinci-003 model\n'
                     '\nFor coding questions select code mode, which using code-davinci-002 model\n'
                     '\nExample:'
                     '\n/code How to write a function in python'
                     '\n/general How are you >')
    elif call.data == "cb_ukrainian":
        bot.send_message(call.message.chat.id, "Привіт! Я ChatGPT telegram бот\n" 'Я використовую модель відповідей GPT-3.5\n' 
                         '\nДля звичайних питань, обирай загальну модель повеіднки, що використовує модель text-davinci-003 model\n'
                         "\nДля питань, що пов'язані з кодом, обирай модель спрямовану на код, що використовує модель code-davinci-002 model\n"
                         '\nНаприклад:'
                         '\n/code Як написати фукнції на python'
                         '\n/general Як твої справи?')
        
@bot.message_handler(commands=['general'], func=lambda message: True)
def generate_text(message):
    response = openai.Completion.create(
        engine=general_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=temperature
)
    generated_text = response.choices[0].text

    bot.reply_to(message, generated_text)
    
@bot.message_handler(commands=['code'], func=lambda message: True)
def generate_text(message):
    response = openai.Completion.create(
        engine=code_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=temperature
)
    generated_text = response.choices[0].text

    bot.reply_to(message, generated_text)

bot.polling()