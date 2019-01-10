from app import Bot
from os import environ

swear_bot = Bot(environ['API_TOKEN'])
swear_bot.run()
