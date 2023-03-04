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
temperature = 0.7

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
                     '\nUsing a text-davinci-003 model\n')
    elif call.data == "cb_ukrainian":
        bot.send_message(call.message.chat.id, "Привіт! Я ChatGPT telegram бот\n" 'Я використовую модель відповідей GPT-3.5\n' 
                         '\nПитання обробляються моделью text-davinci-003\n')

        
@bot.message_handler(func=lambda message: True)
def general_text(message):
    response = openai.Completion.create(
        engine=general_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=temperature
)
    general_text = response.choices[0].text

    bot.reply_to(message, general_text)
    

bot.polling()