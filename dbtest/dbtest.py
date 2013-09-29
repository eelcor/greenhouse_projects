import sqlite3, random, time
from datetime import datetime


class templogger():
	def __init__(self, filename):
		global db
		db = sqlite3.connect(filename)
		db.execute("CREATE TABLE IF NOT EXISTS temp_series(date datetime, event TEXT, value REAL, detail TEXT)")	
		db.commit()

	def measure(self):
		thisdate = datetime.now()
		db.execute(
		'INSERT INTO temp_series(date, event, value, detail) VALUES(?,?,?,?)',
		(
			thisdate,
			"Random number",
			random.randint(0,1000),
			"Gibberish"
		)
		)
		db.commit()

if __name__ == '__main__':
	tempseries = templogger('tempseries')
	while 1:
		tempseries.measure()
		time.sleep(5)

