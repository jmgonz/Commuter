import time
import board
import busio
import adafruit_gps

def info():
	'''Prints a basic library description'''
	print("Software library for the Commuter+ project.")

def turnOnGPS():
	# GPS Module is set to 9600 baudrate by default
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=300)
	gps = adafruit_gps.GPS(uart, debug=False)

	# Turns on basic GGA and RMC info, inludes location so it should be enough
	gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

	# 1Hz updates
	gps.send_command(b"PMTK220,1000")
	return

def grabLocation():
	# Update gps before every location grab
	gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if  current - last_print >= 1.0:
                last_print = current
                if not gps.has_fix:
                        print("Waiting for fix...")
                        continue
                print("Latitude: {0:.6f} degrees".format(gps.latitude))
                print("Longitude: {0:.6f} degrees".format(gps.longitude))
	return (gps.latitude, gps.longitude)

def main():
	turnOnGPS()
