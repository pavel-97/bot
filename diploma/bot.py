import telebot
import os


TOKEN: str = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
