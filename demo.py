import time
import board
import serial

import adafruit_gps


def gpsTestRun():
	# GPS uses 9600 baudrate by default
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

	gps = adafruit_gps.GPS(uart)
	gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
	# Set update rate to once a second, 1hz
	gps.send_command(b"PMTK220,1000")

	timestamp = time.monotonic()
	while True:
		gps.update()
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

main()
