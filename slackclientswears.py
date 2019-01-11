from slackclient import SlackClient
import threading

message_batch = {}

#allow 10 seconds of rolling bursting
def batchSend(self):
	global message_batch

	if message_batch:
		for channelid in message_batch:
			self.client.rtm_send_message(channelid, message_batch[channelid])
		self.time += (1 / self.currentInterval)
	if(self.currentInterval == self.burstInterval):
		self.time -= (1 / self.bufferInterval)
	else:
		self.time -= (1 / self.burstInterval)

	if(self.time<0):
		self.time = 0

	if self.time > (15 / self.burstInterval):
		self.currentInterval = self.bufferInterval
	else:
		self.currentInterval = self.burstInterval
	message_batch.clear()
	threading.Timer(self.currentInterval, batchSend, [self]).start()


class SlackClientSwears(object):

	def __init__(self, token):
		self.client = SlackClient(token)
		self.userid = {}
		self.username = {}
		self.bufferInterval = 1
		self.burstInterval = .25
		self.currentInterval = .25
		self.time = 0
		threading.Timer(self.currentInterval, batchSend, [self]).start()


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
		if not channelid in message_batch:
			 message_batch[channelid] = ""
		message_batch[channelid] = message_batch[channelid] + ("\n" + message)

