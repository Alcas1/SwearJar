from swearjar import Swearjar
from messageprocessor import MessageProcessor
import time
import re
import datetime 

class Bot(object):

	def __init__(self, client):
		self.client = client
		self.swearjar = Swearjar()
		self.processor = MessageProcessor(self.client, self.swearjar)

	def run(self):
		self.client.connect()
		while True:
			self.processor.process_messages(self.client.getLatestMessage())
			time.sleep(0.10)

	


