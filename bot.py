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
                     '\nGeneral model is text-davinci-003 model\n'
                     '\nFor coding optimize add /code to your question, this will provide you an code-optimized answer, using code-davinci-002 model\n'
                     '\nExample:'
                     '\n/code How to write a function in python'
                     '\nHow are you ?\n'
                     '\nAttention, code_davinci-002 in beta stage, and have low rate limit, which causing no response and bot shutdown')
    elif call.data == "cb_ukrainian":
        bot.send_message(call.message.chat.id, "Привіт! Я ChatGPT telegram бот\n" 'Я використовую модель відповідей GPT-3.5\n' 
                         '\nЗагальні питання обробляються моделью text-davinci-003\n'
                         "\nДля отримання код-оптимізованих відповідей, додайте до свого питання /code, це питання буде обробленне моделью code-davinci-002\n"
                         '\nНаприклад:'
                         '\n/code Як написати фукнції на python'
                         '\nЯк твої справи?\n'
                         '\nУвага, code-davinci-002 знаходиться на стадії бета та має маленький rate limit, що може залишити Вас без відповіді та закрити бота:(')
        
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
    
@bot.message_handler(commands=['code'], func=lambda message: True)
def code_text(message):
    response = openai.Completion.create(
        engine=code_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=temperature
)
    code_text = response.choices[0].text

    bot.reply_to(message, code_text)

bot.polling()