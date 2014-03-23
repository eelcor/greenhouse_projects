#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio
#
# João Paulo Barraca <jpbarraca@gmail.com>
#

from nrf24 import NRF24
import time

pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]

radio = NRF24()
radio.begin(0, 0, 15, 18) #Set CE and IRQ pins
radio.setRetries(15,15)
radio.setPayloadSize(8)
radio.setChannel(0x4c)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.startListening()
radio.stopListening()

radio.printDetails()

buf = ['P', 'I', 'N', 'G']
while True:
    radio.write(buf)
    time.sleep(1)
    print("sent")
