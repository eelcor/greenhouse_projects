#!/usr/bin/python

from smbus import SMBus
import struct
import time

# LM75 i2c address:
addr = 0x4F

i2c1 = SMBus(1)


def parse(t):
   # 9 bits of resolution stored in 2 bytes
   r = t >> 5
   # MSB set?
   if (t & 0x8000):
      # one's complement
      r = (~r & 0x1FF)
      # two's complement
      r = r - 1
      # significance: means negative temp
      r = -r

   r = r / 8.0

   return r

def ctof(t):
   return ((9.0/5.0) * parse(t)) + 32.0


while True:
   temp = i2c1.read_word_data(addr, 0)
   tempA = temp & 0xFF;
   tempB = (temp >> 8) & 0xFF
   temp = (tempA << 8) | tempB

   print "read: %04x = %.1f C (%.1f F)" % (temp, parse(temp), ctof(temp))
   time.sleep(0.5)
