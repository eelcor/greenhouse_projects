from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from Adafruit_BBIO import GPIO
from weather import weather
import thread, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger_base import Item, Average, Base
import datetime
from dateutil import parser

app = Flask(__name__)

@app.route('/')
def home():
	if GPIO.input("P8_10") == GPIO.LOW:
		led1 = 'off'
	else:
		led1 = 'on'
	return render_template('index.html', led1val=led1)
	
@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/switch', methods=['POST'])
def switch():
	led1 = request.form['switch1']
	print(request.form)
	print led1
	if led1 == 'on':
		GPIO.output("P8_10", GPIO.HIGH)
	if led1 == 'off':
		GPIO.output("P8_10", GPIO.LOW)
	return redirect(url_for('home'))

@app.route('/measure')
def measure():
	a=weer.measure()
	return jsonify(a)

@app.route('/debug')
def debug():
	a=session2.query(Item)
	cnt = a.count()
	light = session2.query(Item).get(cnt-2)
	pressure = session2.query(Item).get(cnt-1)
	temp = session2.query(Item).get(cnt) 	
	print light.name+' '+str(light.value)+' lx'
	print pressure.name+' '+str(pressure.value)+' mBar'
	print temp.name+' '+str(temp.value)+' degrees Celsius'
	print 'Total count of records: ' + str(cnt)
	return redirect(url_for('home'))
	
def test_thread(name):
	count = 0
	while 1:
		GPIO.output("P8_16",GPIO.HIGH)
		time.sleep(2)
		a = weer.measure()
		dt = parser.parse(a['time'])
		light = Item(name='light', value=a['light'], timestamp=dt)
		pressure = Item(name='pressure', value=a['pressure'], timestamp=dt)
		temp = Item(name='temp', value=a['temp'], timestamp=dt)
		session.add(light)
		session.add(pressure)
		session.add(temp)
		session.commit()
		GPIO.output("P8_16",GPIO.LOW)
		time.sleep(58)
		print "%s" % (time.ctime(time.time()))

if __name__ == '__main__':
	weer=weather()
	GPIO.setup("P8_10",GPIO.OUT)
	GPIO.setup("P8_16",GPIO.OUT)
	GPIO.output("P8_10", GPIO.LOW)
	GPIO.output("P8_16", GPIO.HIGH)
	engine = create_engine('sqlite:///logbase.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	session2 = DBSession()
	thread.start_new_thread( test_thread, ("Logger thread",) )
    	app.run(host='0.0.0.0')
