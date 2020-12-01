#!/usr/bin/python

# File...... rfid-rw-test.py
# Purpose... System-level test code for the Parallax RFID Read/Write USB Module
# Author.... Joe Grand, Grand Idea Studio, Inc. [www.grandideastudio.com]
# E-mail.... support@parallax.com
# Updated... 20 May 2016

# This program performs a system-level test of the Parallax RFID Read/
# Write USB Module by:
#
# 1) Reading a tag's unique ID
# 2) Writing and verifying a block of data to the tag (tag must be unlocked)
#
# Tested with Python 2.7.11 w/ pySerial 3.0.1 on Mac OS X 10.11.5 and Windows 7 SP1.

# RFID R/W MODULE CONSTANTS
# Commands
# Number of bytes returned in ()
CMD_READ          = 0x01   # Read data from specified address, valid locations 1 to 33 (5)
CMD_WRITE         = 0x02   # Write data to specified address, valid locations 3 to 31 (1)
CMD_LOGIN         = 0x03   # Login to tag with password (1)
CMD_SETPASS       = 0x04   # Change tag's password from old to new (1)
CMD_PROTECT       = 0x05   # Enable/disable password protection (1)
CMD_RESET         = 0x06   # Reset tag (1)
CMD_READ_LEGACY   = 0x0F   # Read unique ID from EM4102 read-only tag (for backwards compatibility w/ Parallax RFID Card Reader, #28140 and #28340) (12)

# Memory map/address locations for EM4x50 tag
# Each address holds/returns a 32-bit (4 byte) value
ADDR_PASSWORD     = 0      # Password (not readable)
ADDR_PROTECT      = 1      # Protection Word
ADDR_CONTROL      = 2      # Control Word
# ADDR 3-31 are User EEPROM area
ADDR_SERIAL      = 32      # Device Serial Number
ADDR_DEVICEID    = 33      # Device Identification

# Status/error return codes
ERR_OK           = 0x01    # No errors
ERR_LIW          = 0x02    # Did not find a listen window
ERR_NAK          = 0x03    # Received a NAK, could be invalid command
ERR_NAK_OLDPW    = 0x04    # Received a NAK sending old password (CMD_SETPASS), could be incorrect password
ERR_NAK_NEWPW    = 0x05    # Received a NAK sending new password (CMD_SETPASS)
ERR_LIW_NEWPW    = 0x06    # Did not find a listen window after setting new password (CMD_SETPASS)
ERR_PARITY       = 0x07    # Parity error when reading data

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
      
import os
import sys
import serial  # http://pyserial.sourceforge.net/
import time

# change port name to match your particular instance
# port = "/dev/tty.usbserial-AI05BXXH"    # OS X
port = "//./COM3"                      # Windows

ser = serial.Serial(port, 9600, timeout = None)    # open serial port
sys.stdout = Unbuffered(sys.stdout)                # open stdout in unbuffered mode (automatically flush after each print operation)

print("Parallax RFID Read/Write USB Module Test Application\n")

print("Reading tag's unique serial number...")
while True:
  ser.write(('!RW' + chr(CMD_READ) + chr(ADDR_SERIAL)).encode())    # send command
  buf = ser.read(5)           # get bytes (will block until received)  
  if buf[0] == chr(ERR_OK):   # if valid data received with no error, continue
    break
  print(buf[0], buf[1], buf[2], buf[3], buf[4])
  time.sleep(1)
for i in range(1,len(buf)):   # display data
  sys.stdout.write("%02X" % ord(buf[i]))
print("")

# print("Writing and verifying data to tag...")
# while True:
#   ser.write('!RW' + chr(CMD_WRITE) + chr(3) + '\xFE\xED\xBE\xEF')    # send command, write 4-byte string into address 3 (User EEPROM area)
#   buf = ser.read(1)           # get byte (will block until received)  
#   if buf[0] == chr(ERR_OK):   # if no error, continue
#     break
# print("Success!")

print("End of test.")
ser.close()
