from slackclient import SlackClient


class SlackClientSwears(object):

	def __init__(self, token):
		self.client = SlackClient(token)
		self.userid = {}
		self.username = {}

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
		self.client.api_call(
			"chat.postMessage",
			as_user="true",
			channel=channelid,
			text=message)