from smbus import SMBus
import time

i2c = SMBus(1)
bmp180 = 0x77
#Calibration registers

def read_16bit_regu(address, register):
	a = i2c.read_byte_data(address, register)
	b = i2c.read_byte_data(address, register+1)
	return ((a << 8) | b)

def read_16bit_regs(address, register):
	a = i2c.read_byte_data(address, register)
	b = i2c.read_byte_data(address, register+1)
	c = (a << 8)|b
	if (c & 0x8000):
		c = (~c & 0xffff)
		c = c-1
		c = -c
	return c

def calibration():
	global cal_AC1
	global cal_AC2
	global cal_AC3
	global cal_AC4
	global cal_AC5
	global cal_AC6
	global cal_B1
	global cal_B2
	global cal_MB
	global cal_MC
	global cal_MD
	cal_AC1 = read_16bit_regs(bmp180, 0xaa)
	cal_AC2 = read_16bit_regs(bmp180, 0xac)
	cal_AC3 = read_16bit_regs(bmp180, 0xae)
	cal_AC4 = read_16bit_regu(bmp180, 0xb0)
	cal_AC5 = read_16bit_regu(bmp180, 0xb2)
	cal_AC6 = read_16bit_regu(bmp180, 0xb4)
	cal_B1 = read_16bit_regs(bmp180, 0xb6)
	cal_B2 = read_16bit_regs(bmp180, 0xb8)
	cal_MB = read_16bit_regs(bmp180, 0xba)
	cal_MC = read_16bit_regs(bmp180, 0xbc)
	cal_MD = read_16bit_regs(bmp180, 0xbe)

def printregs():
	print "AC1: %6d" % (cal_AC1)
	print "AC2: %6d" % (cal_AC2)
	print "AC3: %6d" % (cal_AC3)
	print "AC4: %6d" % (cal_AC4)
	print "AC5: %6d" % (cal_AC5)
	print "AC6: %6d" % (cal_AC6)
	print "B1: %6d" % (cal_B1)
	print "B2: %6d" % (cal_B2)
	print "MB: %6d" % (cal_MB)
	print "MC: %6d" % (cal_MC)
	print "MD: %6d" % (cal_MD)

def readRawTemp():
	i2c.write_byte_data(bmp180, 0xf4, 0x2e)
	time.sleep(0.005)
	raw = read_16bit_regu(bmp180, 0xf6)
	return raw

def readTemperature():
	ut = readRawTemp()
	x1 = ((ut - cal_AC6) * cal_AC5) >> 15
	x2 = (cal_MC << 11) / (x1 + cal_MD)
	b5 = x1 + x2
	temp = ((b5 + 8) >> 4)/10.0
	return temp

print("BMP Barometric Pressure Sensor test")
calibration()
print(readRawTemp())
print(readTemperature())
printregs()
