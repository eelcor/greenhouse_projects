#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, thread
import datetime
from nrf24 import NRF24
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify

#nRF24L01 Setup
def radio_setup(pipe_tx,pipe_rx):
	radio = NRF24()
	radio.begin(0,0,22, 23) #Set CE and IRQ pins
	radio.setRetries(15,15) #zeit zwischen retries (x * 250mikro s) und anzahl an retries
	radio.setPayloadSize(16) #32-byte payload
	radio.setChannel(0x4c) #0-127 in hex
	radio.setDataRate(NRF24.BR_250KBPS) 
	radio.setPALevel(NRF24.PA_MAX) #power amplifier level
	radio.openWritingPipe(pipe_tx) 
	radio.openReadingPipe(1,pipe_rx)
	radio.printDetails() #Debug
	print(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + " ------ PyNRF start ------")
	return radio

def receiveloop(name,radio):
	radio.startListening()
	data = []
	x_old = 0
	t_old = 0
	global power, kwh, timestamp
	timestamp = datetime.datetime.utcnow()
	while True:
		if (radio.available()):
			t_new = time.time()
			timestamp = datetime.datetime.utcnow()
			radio.read(data)
			text = u''
			for i in data:
				text += unichr(i)
			x_new = int(text[:11])
			power = 7200*(x_new-x_old)/(t_new-t_old)
			kwh = x_new/500
			x_old = x_new
			t_old = t_new
			print("New value received: "+str(x_new))

def printresults(name):
	while True:
		print "Current used power is: "+str(power)+" Watt"
		print "Total usage is: " +str(kwh)+" KWh"
		time.sleep(10)

# The flask handlers
app = Flask(__name__)

@app_route('/')
def home():
	return render_template('index.html')
	
@app_route('/measure')
def measure():
	value = {'time':str(timestamp),'power':power,'consumption':kwh}
	return jsonify(value)

# The main routine
if __name__ == '__main__':		
	pipes = [ [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xD2] ] #40-bit hex adressen der pipes
	radio = radio_setup(pipes[0], pipes[1])

	#init variables
	kwh = 0
	power = 0

	#init threads
	print("Starting display loop...")
	thread.start_new_thread(printresults, ("Output",))
	print("Display loop started...")
	print("Starting receive loop...")
	thread.start_new_thread(receiveloop, ("Radio",radio,))
	print("Receive loop started...")
	#init webserver
	app.run(host='0.0.0.0')
	
