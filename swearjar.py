from swearlist import swears
from postgres_conn import Postgres
import urlparse 
import redis
import os
import math

class Swearjar(object):
	defaultSwearIncrement = 1

	def __init__(self):
		self.swearlist = swears
		self.defaultMultiplier = 0.25
		self.storage = Postgres()
		self.userSwearCountCache = {}

	def hasSwear(self, text):
		return set(text.split()) & self.swearlist

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
		money = self.checkSwearJar(user) * self.defaultMultiplier
		return math.ceil(money * 100) / 100