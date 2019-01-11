from swearlist import swears
from batch_postgres import BatchPostgres
from profanity_check import predict, predict_prob
import os
import math

class Swearjar(object):
	defaultSwearIncrement = 1

	def __init__(self):
		self.swearlist = swears
		self.defaultMultiplier = 0.25
		self.storage = BatchPostgres()
		self.userSwearCountCache = {}

	def hasSwear(self, text):
		result = predict_prob([text])
		return result > 0

		#return set(x.lower() for x in text.split()) & self.swearlist

	def getSwearList(self):
		return self.swears

	def addToSwearJar(self, user, swearIncrement = defaultSwearIncrement):
		swearCount = self.storage.incrementSwearCount(user, swearIncrement)
		self.userSwearCountCache[user] = swearCount
		return swearCount

	def checkSwearJar(self, user):
		if user in self.userSwearCountCache:
			return self.userSwearCountCache[user]
		return self.storage.getSwearCount(user)

	def getMoneyOwed(self, user):
		return self.swearsToDollarAmount(self.checkSwearJar(user))
		 
	def addNewUser(self, userinfo):
		return self.storage.addNewUser(userinfo)

	def getUserData(self, user):
		return self.storage.getUserData(user)

	def getAllBalances(self):
		swearCounts = self.storage.getAllUserSwearCounts()
		balances = "Balances: \n"
		for userSwearCount in swearCounts:
			balances += "%s: $%.2f\n" % (userSwearCount[1], self.swearsToDollarAmount(userSwearCount[2]))
			self.userSwearCountCache[userSwearCount[0]] = userSwearCount[2] 
		return balances

	def swearsToDollarAmount(self, swears):
		 money = swears * self.defaultMultiplier
		 return math.ceil(money * 100) / 100
