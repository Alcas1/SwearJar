import os
import psycopg2
import threading

# Table name: Jar
# string userid [PRIMARY KEY], string username, string realname, int amount



DATABASE_URL = os.environ['HEROKU_POSTGRESQL_JADE_URL']

insert_batch = {}
update_batch = {}

def batchSend(self):
	global insert_batch
	global update_batch

	if insert_batch:
		insert_query = "insert into swearjar VALUES "
		for userid in insert_batch:
			insert_query += (" ('%s', '%s', '%s', %s)," % 
				(userid,
				insert_batch[userid][0],
				insert_batch[userid][1],
				0))
		try:
			self.cur.execute(insert_query[:-1])
			self.conn.commit()
			insert_batch.clear()
		except psycopg2.Error as e:
			print(e.pgerror)

	if update_batch:
		update_query = "update swearjar as jar set swearcount = updates.swearcount from(values "
		for userid in update_batch:
			update_query += (" ('%s', %s)," %
				(userid, update_batch[userid]))
		update_query = update_query[:-1]
		update_query += ") as updates(userid,swearcount) where updates.userid = jar.userid"
		try:
			self.cur.execute(update_query)
			self.conn.commit()
			update_batch.clear()
		except psycopg2.Error as e:
			print(e.pgerror)

	print("ping")
	threading.Timer(self.batch_interval, batchSend, [self]).start()


class BatchPostgres(object):

	def __init__(self):
		self.conn = psycopg2.connect(DATABASE_URL)
		self.cur = self.conn.cursor()
		self.batch_interval = 30
		threading.Timer(self.batch_interval, batchSend, [self]).start()

	def incrementSwearCount(self, user, swearIncrement):

		swearcount = self.getSwearCount(user)
		finalcount = swearcount + swearIncrement
		update_batch[user] = finalcount
		return finalcount

	def getSwearCount(self, user):
		if user in update_batch:
			return update_batch[user]
		else:
			swearcount = self.getUserData(user)
			if swearcount is None:
				return 0
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
			print("can't find users")
			print(e)

	def addNewUser(self, user_info):
		insert_batch[user_info["id"]] = (user_info["name"], user_info["real_name"])
