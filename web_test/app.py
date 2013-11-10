from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from Adafruit_BBIO import GPIO

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

@app.route('/get_data_1day')
def get_data_1day():
	a={'dataset':[
    {'naam':'Eelco', 'beroep':'consultant'},
    {'naam':'Marije','beroep':'orthopedagoog'},
    {'naam':'Hugo','beroep':'grote broer'}
	]}
	return jsonify(a)

if __name__ == '__main__':
	GPIO.setup("P8_10",GPIO.OUT)
	GPIO.output("P8_10", GPIO.LOW)
    	app.run(host='0.0.0.0')
