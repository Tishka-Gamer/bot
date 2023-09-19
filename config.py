import telebot
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='dd76278d71804462b39484a6d22d1326')


bot = telebot.TeleBot("5878687382:AAE7AtGkcFShrZ9_AwVZoKAWxd0u1FhGtqU", parse_mode=None)