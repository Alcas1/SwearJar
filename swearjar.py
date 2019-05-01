from swearlist import swears
from batch_postgres import BatchPostgres
import spacy
from profanity_filter import ProfanityFilter, AVAILABLE_ANALYSES
import os
import math

class Swearjar(object):
	defaultSwearIncrement = 1

	def __init__(self):
		self.swearlist = swears
		self.defaultMultiplier = 0.25
		self.storage = BatchPostgres()
		self.userSwearCountCache = {}
		self.nlp = spacy.load('en')
		filter = ProfanityFilter(nlps={'en': self.nlp})
		self.nlp.add_pipe(filter.spacy_component, last=True)
		print(', '.join(sorted(analysis.value for analysis in AVAILABLE_ANALYSES)))


	def hasSwear(self, text):
		doc = self.nlp(text)
		# for token in doc:
		# 	print(f'{token}:'
		# 		f'censored={token._.censored}, '
		# 		f'is_profane={token._.is_profane}, '
		# 		f'original_profane_word={token._.original_profane_word}'
		# 	)

		return doc._.is_profane
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
