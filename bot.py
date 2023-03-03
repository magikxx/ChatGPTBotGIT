import os
import telebot
import openai
import dotenv
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

model_engine = "text-davinci-003"
max_tokens = 1024
temperature = 0.2

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Hello! Im ChatGPT telegram bot\n" "Ask me anything, and I will respond ASAP")
    
@bot.message_handler(func=lambda message: True)
def generate_text(message):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=temperature
    )
    generated_text = response.choices[0].text

    bot.reply_to(message, generated_text)

bot.polling()