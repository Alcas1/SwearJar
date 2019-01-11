from slackclient import SlackClient
import threading

message_batch = str()
channel_id = ""

def batchSend(self):
	global message_batch
	global channel_id

	if len(message_batch) > 0:
		self.client.rtm_send_message(channel_id, message_batch)
		message_batch = ""
	threading.Timer(self.bufferInterval, batchSend, [self]).start()


class SlackClientSwears(object):

	def __init__(self, token):
		self.client = SlackClient(token)
		self.userid = {}
		self.username = {}
		self.bufferInterval = 1
		threading.Timer(self.bufferInterval, batchSend, [self]).start()


	def connect(self):
		if self.client.rtm_connect():
			try:
				self.userid = self.client.api_call("auth.test")['user_id']
				self.username = self.client.api_call("auth.test")['user']
				print("Connected: " + self.username + ": " + self.userid)

			except Exception as e:
				print(e)
		else:
			print("Connection failed.")

	def getLatestMessage(self):
		return self.client.rtm_read()

	def getUserInfo(self, userid):
		return self.client.api_call("users.info", user = userid)["user"]

	def isBotUser(self, userid):
		return userid == self.userid

	def checkMention(self, message):
		return self.userid in message

	def postBotMessage(self, message, channelid):
		global message_batch
		global channel_id

		message_batch = message_batch + ("\n" + message)
		channel_id = channelid

