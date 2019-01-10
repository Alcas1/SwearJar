

class MessageProcessor(object):

	def __init__(self, client, swearjar):
		self.client = client
		self.swearjar = swearjar

	def process_messages(self, messages):
		for msg in messages:
			if msg['type'] == "message":
				if 'text' in msg:
					body = msg.get('text')
					if(self.swearjar.hasSwear(body)):
						self.process_swear_message(body, msg["user"])
						
	def process_swear_message(self, swear_message, userid):
		swears = 0
		user_data = self.swearjar.getUserData(userid)
		userinfo = self.client.getUserInfo(userid)

		if user_data is None:
			self.swearjar.addNewUser(userinfo)

		swears = self.swearjar.addToSwearJar(userid)

		if self.client.isBotUser(userid):
			message = ("sorry "
				+ userinfo["name"]
				+ " this is a christian channel, so no swearing. "
				+ userinfo["name"]
				+ " now owes: $"
				+ ("%.2f" % self.swearjar.getMoneyOwed(userid)))
			self.client.postBotMessage(message)