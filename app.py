from slackclient import SlackClient
from swearjar import Swearjar
import time
import re
import datetime 

class Bot(object):

	def __init__(self, token):
		self.client = SlackClient(token)
		self.username = {}
		self.user_id = {}
		self.channel_id = "GDTAPGV1T" 
		self.swearjar = Swearjar()

	def run(self):
		if self.client.rtm_connect():
			try:
				self.user_id = self.client.api_call("auth.test")['user_id']
				self.username = self.client.api_call("auth.test")['user']
				print self.username + ": " + self.user_id

			except Exception as e:
				print e
			while True:
				self.process_messages(self.client.rtm_read())
				time.sleep(0.25)
		else:
			print "Connection failed."

	def process_messages(self, messages):
		for msg in messages:
			if msg['type'] == "message":
				if 'text' in msg:
					body = msg.get('text')
					print body
					if(self.swearjar.hasSwear(body)):
						swears = 0
						userid = msg["user"]
						user_data = self.swearjar.storage.getUserData(userid)
						userinfo = self.client.api_call("users.info", user = userid)["user"]
						if user_data is None:
							self.swearjar.storage.addNewUser(userinfo)

						swears = self.swearjar.addToSwearJar(msg["user"])

						if msg.get('user') != self.user_id:
							self.client.api_call(
								"chat.postMessage", 
								as_user="true",
								channel=msg['channel'],
								text="sorry "
									+ userinfo["name"]
									+ " this is a christian channel, so no swearing. "
									+ userinfo["name"]
									+ " now owes: $"
									+ ("%.2f" % self.swearjar.getMoneyOwed(userid)))
