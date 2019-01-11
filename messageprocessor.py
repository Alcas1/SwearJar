

class MessageProcessor(object):

	def __init__(self, client, swearjar):
		self.client = client
		self.swearjar = swearjar

	def process_messages(self, messages):
		for msg in messages:
			if 'text' in msg and 'type' in msg:
				if msg['type'] == "message":
					channelid = msg["channel"]
					body = msg.get('text')
					body_words = body.split()
					userid = msg.get("user")
					if(userid is None):
						return

					if self.client.checkMention(body_words[0]):
						if(len(body_words) > 1):
							command_func = self.checkForCommands(body_words[1])
							command_func(body, userid, channelid)
						else: 
							self.client.postBotMessage("Remember, this is a Christian channel. So NO SWEARING.", channelid)
					elif self.swearjar.hasSwear(body):
						self.process_swear_message(body, userid, channelid)
						
	def checkForCommands(self, command):
		run_commands = {
			"balance":self.process_balance,
			"balances":self.process_balance
		}
		return run_commands.get(command, self.unknown_command)

	def process_balance(self, command, userid, channelid):
		balances = self.swearjar.getAllBalances()
		self.client.postBotMessage(balances, channelid)

	def unknown_command(self, command, userid, channelid):
		if self.swearjar.hasSwear(command):
			self.process_swear_message(command, userid, channelid)
		else:
			self.client.postBotMessage("Remember, this is a Christian channel. So NO SWEARING.", channelid)


	def process_swear_message(self, swear_message, userid, channelid):
		swears = 0
		user_data = self.swearjar.getUserData(userid)
		userinfo = self.client.getUserInfo(userid)

		if user_data is None:
			self.swearjar.addNewUser(userinfo)

		swears = self.swearjar.addToSwearJar(userid)

		if not self.client.isBotUser(userid):
			message = ("sorry "
				+ userinfo["name"]
				+ " this is a christian channel, so no swearing. "
				+ userinfo["name"]
				+ " now owes: $"
				+ ("%.2f" % self.swearjar.getMoneyOwed(userid)))
			self.client.postBotMessage(message, channelid)