from app import Bot
from slackclientswears import SlackClientSwears
from os import environ


client = SlackClientSwears(environ['API_TOKEN'])
swear_bot = Bot(client)
swear_bot.run()

#randomest id "GDTAPGV1T"