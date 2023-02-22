import time
import board
import busio
import serial

import adafruit_gps

# Chip uses 9600 baudrate by default
def gpsTestRun():
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

	gps = adafruit_gps.GPS(uart)
	gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second, 1hz
	gps.send_command(b"PMTK220,1000")

	timestamp = time.monotonic()
	while True:
        	data = gps.read(32) # Reads up to 32 bytes

	        if data is not None:
        	        data_string = "".join([chr(b) for b in data])
                	print(data_string, end="")


        	if time.monotonic() - timestamp >5:
                	# This will run every 5 seconds
                	gps.send_command(b"PMTK605") # Requests firmware version
                	timestamp = time.monotonic()
def main():
	gpsTestRun()

