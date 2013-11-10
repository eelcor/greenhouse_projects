from Adafruit_BBIO import GPIO
from  weather import weather
import time

GPIO.setup("P8_10", GPIO.OUT)
weer = weather()
while 1:
	weer.print_climate()
	GPIO.output("P8_10", GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output("P8_10", GPIO.LOW)
	time.sleep(1)
