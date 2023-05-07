#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont
import time,random

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
heartrate=85
status=True
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

def update_hr(heartrate):
	temp=random.randint(-5,7)
	if ((heartrate+temp)<130) and ((heartrate+temp)>60):
		heartrate=heartrate+temp
	return heartrate

def buttonone(heartrate):
	try:
		# display with hardware SPI:
		''' Warning!!!Don't  creation of multiple displayer objects!!! >'''
		#disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi>
		disp = LCD_1inch28.LCD_1inch28()
		# Initialize library.
		disp.Init()
		image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
		draw = ImageDraw.Draw(image1)
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
		time.sleep(5)
	except IOError as e:
		logging.info(e)    
	except KeyboardInterrupt:
		disp.module_exit()
		logging.info("quit:")
		exit()
	return heartrate

def buttontwo(status):
	if (status):
		disp=LCD_1inch28.LCD_1inch28()
		disp.Init()
		disp.clear()
		image1=Image.new("RGB",(disp.width,disp.height),"BLACK")
		draw=ImageDraw.Draw(image1)
		disp.ShowImage(image1)
		time.sleep(10)
		status=not status
	else:
		lcd(heartrate)
		status=not status

while 1:
	heartrate=update_hr(heartrate)
	lcd(heartrate)
	buttonone(heartrate)
	buttontwo(heartrate)

