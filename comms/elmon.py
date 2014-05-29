#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, sys
from nrf24 import NRF24

pipes = [ [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xD2] ] #40-bit hex adressen der pipes

#nRF24L01 Setup
radio = NRF24()
radio.begin(0,0,22, 23) #Set CE and IRQ pins
radio.setRetries(15,15) #zeit zwischen retries (x * 250mikro s) und anzahl an retries
radio.setPayloadSize(16) #32-byte payload
radio.setChannel(0x4c) #0-127 in hex
radio.setDataRate(NRF24.BR_250KBPS) 
radio.setPALevel(NRF24.PA_MAX) #power amplifier level
radio.openWritingPipe(pipes[0]) 
radio.openReadingPipe(1,pipes[1])
radio.printDetails() #Debug
print(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + " ------ PyNRF start ------")

try:
    # main code
    radio.startListening()
    data = []
    x_old = 0
    t_old = 0
    while True:
		if(radio.available()):
			t_new = time.time()
			radio.read(data)
			text = u''
			for i in data:
				text += unichr(i)
			x_new = int(text[:11])
			power = 7200*(x_new-x_old)/(t_new-t_old)
			kwh = x_new/500
			print 'Current consumption: '+str(power)+' Watt'
			print 'Total consumption: '+str(kwh)+' KWh'
			x_old = x_new
			t_old = t_new
			radio.flush_rx()
	
except KeyboardInterrupt:
    sys.exit(0)
