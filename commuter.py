import board
import adafruit_gps
#import chardet
import os, sys, time, logging, random
import os.path
import BLEHeartRateLogger
# import sys
# import time
# import logging
import spidev as SPI
import RPi.GPIO as GPIO
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
screenStatus = True
heartrate = 85
logging.basicConfig(level=logging.DEBUG)
def lcd(heartrate):
	try:
		# display with hardware SPI:
		''' Warning!!!Don't  creation of multiple displayer objects!!! '''
		#disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
		disp = LCD_1inch28.LCD_1inch28()
		# Initialize library.
		disp.Init()
		# Clear display.
		#disp.clear()

		# Create blank image for drawing.
		image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
		draw = ImageDraw.Draw(image1)

		#logging.info("draw point")
		#draw.rectangle((Xstart,Ystart,Xend,Yend), fill = "color")
		if (heartrate<100):

			logging.info("draw circle")
			draw.arc((1,1,239,239),0, 360, fill =(0,255,0))
			draw.arc((2,2,238,238),0, 360, fill =(0,255,0))
			draw.arc((3,3,237,237),0, 360, fill =(0,255,0))
		else:
			logging.info("draw circle")
			draw.arc((1,1,239,239),0, 360, fill =(255,0,0))
			draw.arc((2,2,238,238),0, 360, fill =(255,0,0))
			draw.arc((3,3,237,237),0, 360, fill =(255,0,0))

		logging.info("draw text")
		Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
		Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
		Font3 = ImageFont.truetype("../Font/Font02.ttf",32)
		text= u"Heart Rate: "+str(heartrate)
		draw.text((40, 95),text, fill = "WHITE",font=Font3)
 
		im_r=image1.rotate(180)
		disp.ShowImage(im_r)
		time.sleep(2)
		#disp.clear()
		#image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
		#draw = ImageDraw.Draw(image1)
		#disp.ShowImage(image1)
		#disp.module_exit()
		#logging.info("quit:")
		#exit()

	except IOError as e:
		logging.info(e)    
	except KeyboardInterrupt:
		disp.module_exit()
		logging.info("quit:")
		exit()


def info():
    '''Prints a basic library description'''
    print("Software library for the Commuter project.")

def turnOnLCD():
	# Raspberry Pi pin configuration:
	RST = 27
	DC = 25
	BL = 18
	bus = 0
	device = 0
	logging.basicConfig(level=logging.DEBUG)
	try:
		# display with hardware SPI:
		''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    	#disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
		disp = LCD_1inch28.LCD_1inch28()
    	# Initialize library.
		disp.Init()
    	# Clear display.
		disp.clear()

    	# Create blank image for drawing.
		image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
		draw = ImageDraw.Draw(image1)

    	#logging.info("draw point")
    	#draw.rectangle((Xstart,Ystart,Xend,Yend), fill = "color")
		logging.info("draw circle")
		draw.arc((1,1,239,239),0, 360, fill =(0,0,255))
		draw.arc((2,2,238,238),0, 360, fill =(0,0,255))
		draw.arc((3,3,237,237),0, 360, fill =(0,0,255))


		logging.info("draw text")
		Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
		Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
		Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

		text= u"Heart Rate: 99"
		draw.text((40, 95),text, fill = "WHITE",font=Font3)
		im_r=image1.rotate(180)
		disp.ShowImage(im_r)
		time.sleep(10)

    	#disp.ShowImage(im_r)
    	#time.sleep(1)
    	#disp.module_exit()
    	#logging.info("quit:")
	except IOError as e:
		logging.info(e)
	except KeyboardInterrupt:
		disp.module_exit()
		logging.info("quit:")
		exit()


def turnOnGPS():
	# GPS Module is set to 9600 baudrate by default so the UART is set to match
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
	global gps
	gps = adafruit_gps.GPS(uart, debug=False)

	# Turns on basic GGA and RMC info, inludes location so it should be enough
	gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

	# 1Hz update rate
	gps.send_command(b"PMTK220,1000")
	return


def grabLocation():
	# Update gps before every location grab
	gps.update()

	if gps.has_fix: # Fix found
		print("Latitude: {0:.6f} degrees".format(gps.latitude))
		print("Longitude: {0:.6f} degrees".format(gps.longitude))
		return (gps.latitude, gps.longitude, gps.timestamp_utc.tm_mday,
					gps.timestamp_utc.tm_mon,
					gps.timestamp_utc.tm_year,
					gps.timestamp_utc.tm_hour,
					gps.timestamp_utc.tm_min,
					gps.timestamp_utc.tm_sec)
					
	else: # No fix
		print("Waiting for fix...")
		return "NO FIX"


	


def writeData(userData):
	# If the file exists append to it
	if os.path.isfile("./userdata.txt"):
		f = open("userdata.txt", "a")
	else: # Else create it
		f = open("userdata.txt", "w")
		f.write("Time, Heart rate, Latitude, Longtitude, Manual")
	f.write(userData)
	f.close()


def screenToggle():
	if (screenStatus):
		disp=LCD_1inch28.LCD_1inch28()
		disp.Init()
		disp.clear()
		image1=Image.new("RGB",(disp.width,disp.height),"BLACK")
		draw=ImageDraw.Draw(image1)
		disp.ShowImage(image1)
		time.sleep(10)
		screenStatus=not screenStatus
	else:
		lcd(heartrate)
		screenStatus=not screenStatus


def setup():
	GPIO.setmode(GPIO.BCM)
	global stressPin
	global screenPin
	global motorPin

	stressPin = 23
	screenPin = 24
	motorPin = 16

	GPIO.setup(stressPin, GPIO.IN)
	GPIO.setup(screenPin, GPIO.IN)
	GPIO.setup(motorPin, GPIO.OUT)

	turnOnGPS()
	turnOnLCD()


def turnOnMotor():
	# Vibrates twice in half second intervals to give user feedback on button press
	GPIO.output(motorPin, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(motorPin, GPIO.LOW)
	time.sleep(0.5)

	GPIO.output(motorPin, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(motorPin, GPIO.LOW)


def stressButton():
	while True:
		GPIO.wait_for_edge(stressPin, GPIO.RISING)
		turnOnMotor()


def screenButton():
	while True:
		GPIO.wait_for_edge(screenButton, GPIO.RISING)
		screenToggle()


def main():
	setup()
