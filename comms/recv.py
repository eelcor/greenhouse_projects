#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio
#
# João Paulo Barraca <jpbarraca@gmail.com>
#
from nrf24 import NRF24
import time

pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]

radio = NRF24()
radio.begin(0, 0, 22, 23)

radio.setRetries(15,15)

radio.setPayloadSize(8)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(1)

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.startListening()
radio.stopListening()

radio.printDetails()

radio.startListening()

while True:
    pipe = [0]
    while not radio.available(pipe, True):
        time.sleep(1000/1000000.0)

    recv_buffer = []
    radio.read(recv_buffer)

    print recv_buffer
