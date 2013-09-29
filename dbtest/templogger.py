import sqlite3, random, time
from smbus import SMBus
from datetime import datetime


class templogger():
	_cal_AC1 = 0
	_cal_AC2 = 0
	_cal_AC3 = 0
	_cal_AC4 = 0
	_cal_AC5 = 0
	_cal_AC6 = 0
	_cal_B1 = 0
	_cal_B2 = 0
	_cal_MB = 0
	_cal_MC = 0
	_cal_MD = 0
	bmp180 = 0
	bh1750 = 0
	lm75addr = 0
	i2c1 = 0
	db = 0
		

	def __init__(self, filename):
		self.i2c1 = SMBus(1)
		self.lm75addr = 0x4f
		self.db = sqlite3.connect(filename)
		self.db.execute("CREATE TABLE IF NOT EXISTS temp_series(date datetime, event TEXT, value REAL, detail TEXT)")	
		self.db.commit()
		self.calibration()
		self.bmp180 = 0x77
		self.bh1750 = 0x23
		self.calibration()
		
	def calibration(self):
		self._cal_AC1 = self.read_16bit_regs(self.bmp180, 0xaa)
		self._cal_AC2 = self.read_16bit_regs(self.bmp180, 0xac)
		self._cal_AC3 = self.read_16bit_regs(self.bmp180, 0xae)
		self._cal_AC4 = self.read_16bit_regu(self.bmp180, 0xb0)
		self._cal_AC5 = self.read_16bit_regu(self.bmp180, 0xb2)
		self._cal_AC6 = self.read_16bit_regu(self.bmp180, 0xb4)
		self._cal_B1 = self.read_16bit_regs(self.bmp180, 0xb6)
		self._cal_B2 = self.read_16bit_regs(self.bmp180, 0xb8)
		self._cal_MB = self.read_16bit_regs(self.bmp180, 0xba)
		self._cal_MC = self.read_16bit_regs(self.bmp180, 0xbc)
		self._cal_MD = self.read_16bit_regs(self.bmp180, 0xbe)

	def readRawTemp(self):
		self.i2c1.write_byte_data(self.bmp180, 0xf4, 0x2e)
		time.sleep(0.005)
		raw = self.read_16bit_regu(self.bmp180, 0xf6)
		return raw

	def readTemperature(self):
		ut = self.readRawTemp()
		x1 = ((ut - self._cal_AC6) * self._cal_AC5) >> 15
		x2 = (self._cal_MC << 11) / (x1 + self._cal_MD)
		b5 = x1 + x2
		temp = ((b5 + 8) >> 4)/10.0
		return temp
	
	def readRawPressure(self):
		self.i2c.write_byte_data(self.bmp180, 0xf4, 0xf4) #Read ultra high resolution
		time.sleep(0.026)
		msb = self.i2c.read_byte_data(self.bmp180, 0xf6)
		lsb = self.i2c.read_byte_data(self.bmp180, 0xf7)
		xlsb = self.i2c.read_byte_data(self.bmp180, 0xf8)
		raw = (msb << 16) + (lsb << 8) + (xlsb) >> 5
		return raw
	
	def readPressure(self):
		ut = self.readRawTemp()
		up = self.readRawPressure()
		x1 = ((ut - self._cal_AC6) * self._cal_AC5) >> 15
		x2 = (self._cal_MC << 11) / (x1 + self._cal_MD)
		b5 = x1 + x2
	
		b6 = b5 - 4000
		x1 = (self._cal_B2 * (b6 * b6) >> 12) >> 11
		x2 = (self._cal_AC2 * b6) >> 11
		x3 = x1 + x2
		b3 = (((self._cal_AC1 * 4 + x3) << 3) + 2) / 4
	
		x1 = (self._cal_AC3 * b6) >> 13
		x2 = (self._cal_B1 * ((b6 * b6) >> 12)) >> 16
		x3 = ((x1 + x2) + 2) >> 2
		b4 = (self._cal_AC4 * (x3 + 32768)) >> 15
		b7 = (up - b3) * (50000 >> 3)
	
		if (b7 < 0x80000000):
			p = (b7 * 2) / b4
		else:
			p = (b7 / b4) * 2
		print(p)
	
		x1 = (p >> 8) * (p >> 8)
		x1 = (x1 * 3038) >> 16
		x2 = (-7357 * p) >> 16
		p = p + ((x1 + x2 + 3791) >> 4)
		return p

	def readLM75Temperature(self):
		# Measure temperature
		temp = self.i2c1.read_word_data(self.lm75addr,0)
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
		return value

	def readBH1750Light(self):
		# Measure light
		luxtmp = self.i2c1.read_word_data(self.bh1750, 0x10)
		lux = (((luxtmp >> 8) & 0xff) | ((luxtmp & 0xff) << 8))/1.2
		return lux

	def measure(self):
		thisdate = datetime.now()
		print(thisdate)
		value = self.readLM75Temperature()
		self.db.execute(
		'INSERT INTO temp_series(date, event, value, detail) VALUES(?,?,?,?)',
		(
			thisdate,
			"Temperature",
			value,
			"Green House"
		)
		)
		self.db.commit()
		lux = self.readBH1750Light()
		self.db.execute(
		'INSERT INTO temp_series(date, event, value, detail) VALUES(?, ?, ?, ?)',
		(
			thisdate,
			"Light intensity",
			lux,
			"Greenhouse"
		)
		)
		self.db.commit()
	
	def print_climate(self):
		print datetime.now()
		print "The temperature is: %i Degrees Celsius" % (self.readLM75Temperature())
		print "The light intensity is: %i Lux" % (self.readBH1750Light())
		print "The pressure is: %i Pascal" % (self.readPressure())		
	
	def read_16bit_regu(self, address, register):
		a = self.i2c1.read_byte_data(address, register)
		b = self.i2c1.read_byte_data(address, register+1)
		return ((a << 8) | b)

	def read_16bit_regs(self, address, register):
		a = self.i2c1.read_byte_data(address, register)
		b = self.i2c1.read_byte_data(address, register+1)
		c = (a << 8)|b
		if (c & 0x8000):
			c = (~c & 0xffff)
			c = c-1
			c = -c
		return c	

if __name__ == '__main__':
	tempseries = templogger('tempseries')
	while 1:
		#tempseries.measure()
		tempseries.print_climate()
		time.sleep(5)

