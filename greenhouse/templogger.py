import Adafruit_BBIO.GPIO as GPIO
import sqlite3, random, time
from smbus import SMBus
from datetime import datetime


class templogger():
	def __init__(self, filename):
		global i2c1 
		i2c1 = SMBus(1)
		global lm75addr 
		lm75addr = 0x4f
		global db
		GPIO.setup("P8_10", GPIO.OUT)
		db = sqlite3.connect(filename)
		db.execute("CREATE TABLE IF NOT EXISTS temp_series(date datetime, event TEXT, value REAL, detail TEXT)")	
		db.commit()
		luxtmp = i2c1.read_word_data(0x23, 0x10)

	def measure(self):
		thisdate = datetime.now()
		# Measure temperature
		temp = i2c1.read_word_data(lm75addr,0)
		# Swap lower and higher byte
		temp = (((temp & 0xff) << 8)|((temp >> 8) & 0xff))
		value = temp >> 5
		if (temp & 0x8000):
			# one's complement
			value = (~value & 0x1FF)
			# two's complement
			value = value - 1
			# significance: means negative temp
			value = -value
		value = value / 8.0
		db.execute(
		'INSERT INTO temp_series(date, event, value, detail) VALUES(?,?,?,?)',
		(
			thisdate,
			"Temperature",
			value,
			"Green House"
		)
		)
		db.commit()
		# Measure light
		luxtmp = i2c1.read_word_data(0x23, 0x10)
		lux = (((luxtmp >> 8) & 0xff) | ((luxtmp & 0xff) << 8))/1.2
		db.execute(
		'INSERT INTO temp_series(date, event, value, detail) VALUES(?, ?, ?, ?)',
		(
			thisdate,
			"Light intensity",
			lux,
			"Greenhouse"
		)
		)
		db.commit()
			

if __name__ == '__main__':
	tempseries = templogger('tempseries')
	while 1:
		tempseries.measure()
		GPIO.output("P8_10", GPIO.HIGH)
		time.sleep(1)
		GPIO.output("P8_10", GPIO.LOW)
		time.sleep(60)

