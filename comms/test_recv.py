#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, sys
from nrf24 import NRF24

pipes = [ [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xD2] ] #40-bit hex adressen der pipes

#nRF24L01 Setup
radio = NRF24()
radio.begin(2,0,"P8_23","P8_24") #Set CE and IRQ pins
radio.setRetries(15,15) #zeit zwischen retries (x * 250mikro s) und anzahl an retries
radio.setPayloadSize(8) #32-byte payload
radio.setChannel(0x60) #0-127 in hex
radio.setDataRate(NRF24.BR_250KBPS) 
radio.setPALevel(NRF24.PA_MAX) #power amplifier level
radio.openWritingPipe(pipes[0]) 
radio.openReadingPipe(1,pipes[1])
radio.printDetails() #Debug
# radio.startListening()
print(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + " ------ PyNRF start ------")

# main code
data = []
while True:
	text = ''
	data_tx = ['R','0','1','2','3','4','5',0]
	radio.stopListening()
	radio.write(data_tx)
	time.sleep(1.0)
	timer = time.time()
	while (not(text[0:3]=='END') and ((time.time()-timer)<3)):
		print(time.time()-timer)
		timer2 = time.time()
#		if(radio.available()):
#			radio.read(data)
#			text = ''
#			for i in data:
#				text += unichr(i)
#			sys.stdout.write(text)
	
