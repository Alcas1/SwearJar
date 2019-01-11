import os
import psycopg2
from threading import Thread

# Table name: Jar
# string userid [PRIMARY KEY], string username, string realname, int amount

DATABASE_URL = os.environ['HEROKU_POSTGRESQL_JADE_URL']

class Postgres(object):

	def __init__(self):
		self.conn = psycopg2.connect(DATABASE_URL)
		self.cur = self.conn.cursor()
		self.update_interval = 15
		
	def incrementSwearCount(self, user, swearIncrement):
		swearcount = self.getSwearCount(user)
		finalcount = swearcount + swearIncrement
		update_swear_query = "update swearjar set swearcount = %s where userid = %s"
		try:
			self.cur.execute(update_swear_query, (finalcount, user))
			self.conn.commit()
		except psycopg2.Error as e:
			print(e.pgerror)
		return finalcount

	def getSwearCount(self, user):
		return self.getUserData(user)[3]

	def getUserData(self, user):
		find_query = "select * from swearjar where userid = %s"
		try:
			self.cur.execute(find_query, (user,))
			user_data = self.cur.fetchone()
			return user_data
		except psycopg2.Error as e:
			print(e.pgerror)

	def getAllUserSwearCounts(self):
		lookup_query = "select userid, username, swearcount from swearjar"
		try:
			self.cur.execute(lookup_query, ())
			all_user_swearcounts = self.cur.fetchall()
			return all_user_swearcounts
		except psycopg2.Error as e:
			print(e.pgerror)

	def addNewUser(self, user_info):
		add_user_query = "insert into swearjar VALUES(%s, %s, %s, %s)"
		try:
			self.cur.execute(add_user_query, (
				user_info["id"], 
				user_info["name"], 
				user_info["real_name"],
				0))
			self.conn.commit()
		except psycopg2.Error as e:
			print(e.pgerror)
