import Adafruit_BBIO.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, abort, session

app = Flask(__name__)
GPIO.setup("P8_10", GPIO.OUT)
GPIO.output("P8_10", GPIO.HIGH)
GPIO.setup("P8_13", GPIO.IN)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/on')
def light_on():
	GPIO.output("P8_10", GPIO.LOW)
	return render_template('index.html')

@app.route('/off')
def light_off():
	GPIO.output("P8_10", GPIO.HIGH)
	return render_template('index.html')

if __name__=='__main__':
	app.run(host='0.0.0.0')
