#!/usr/bin/python
import tweepy
import os
import subprocess
import time
time.sleep(2) # Time to start the  raspberry os
import smbus
import math
from phue import Bridge
import logging
import RPi.GPIO as GPIO
from picamera import PiCamera
from os import system

camera = PiCamera()

# -------------------------------------
# GPIO INIT
# -------------------------------------

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
logging.basicConfig()

# -------------------------------------
# Connect to your Bridge HUE
# -------------------------------------

b = Bridge('192.168.1.10')
db_brightness={}
db_xy={}
db_on={}
db_restoring={}

# -------------------------------------
# Connect CONSUMER_KEY TWITTER
# -------------------------------------

# Paste your consumer key and consumer secret here
consumer_key = ''
consumer_secret = ''
# Paste access token and access token secret here
access_token = ''
access_token_secret = ''


# b.connect()                  <<  In case of need to sync hue bridge (ex : first time use)

execfile("/home/pi/ledoff.py") # Setting led off (for a reboot finish)

# -------------------------------------
# Flashing HUE Light Functions
# ------------------------------------- 

def flash_green():                                            
    b.set_light([4,8,20,21,22], 'xy', [0.409, 0.518])
    b.set_light([4,8,20,21,22], 'bri', 254)
    b.set_light([4,8,20,21,22], 'bri', 0)
    time.sleep(0.1)

def flash_red():
    b.set_light([4,8,20,21,22], 'xy', [0.675, 0.322])
    b.set_light([4,8,20,21,22], 'bri', 254)
    b.set_light([4,8,20,21,22], 'bri', 0)
    time.sleep(0.1)

# --------------------------------------
# CAT_OUT OR CAT_IN FONCTION DETECTION
# --------------------------------------

def cat_out():
    b.set_light(21, 'on', True)
    b.set_light(21, 'xy', [0.3227, 0.3290])        # <<< Catch and save the current value of light 21 to use it like a flash white light (for good pictures)
    b.set_light(21, 'bri', 254)

    for i in range(10):
        camera.capture('image{0:04d}.jpg'.format(i)) # <<<< Take and save 10 pictures
    b.set_light(21, 'bri', 2)                        # <<<< Take off the flash light after taking pictures
    
    # ---------------------
    # Save all light status
    # ---------------------

    h4 = b.get_light(4, 'hue')
    h8 = b.get_light(8, 'hue')
    h20 = b.get_light(20, 'hue')
    h22 = b.get_light(22, 'hue')

    br4 = b.get_light(4, 'bri')
    br8 = b.get_light(8, 'bri')
    br20 = b.get_light(20, 'bri')
    br22 = b.get_light(22, 'bri')

    p4 = b.get_light(4, 'on')
    p8 = b.get_light(8, 'on')
    p20 = b.get_light(20, 'on')
    p22 = b.get_light(22, 'on')

    # ---------------------
    # Flash 2 times in RED
    # ---------------------

    flash_red()
    execfile("/home/pi/ledoff.py")  # << And turn led off
    flash_red()

    # ---------------------
    # Put back all light status
    # ---------------------

    b.set_light(4,'hue',h4)
    b.set_light(8,'hue',h8)
    b.set_light(20,'hue',h20)
    b.set_light(21,'hue',h21)
    b.set_light(22,'hue',h22)

    b.set_light(4,'bri',br4)
    b.set_light(8,'bri',br8)
    b.set_light(20,'bri',br20)
    b.set_light(21,'bri',br21)
    b.set_light(22,'bri',br22)

    b.set_light(4,'on',p4)
    b.set_light(8,'on',p8)
    b.set_light(20,'on',p20)
    b.set_light(21,'on',p21)
    b.set_light(22,'on',p22)

    execfile("/home/pi/Pi-Tweeter/tweet.py")  # << We already save 10 pictures, now we need to tweet it like a GIF
    time.sleep(7)                             # << This sleep is using to signal cat_out cannot be catch 2 times

def cat_in():
    b.set_light(21, 'on', True)
    b.set_light(21, 'xy', [0.3227, 0.3290])   # <<< Catch and save the current value of light 21 to use it like a flash white light (for good pictures)
    b.set_light(21, 'bri', 254)

    i = 0
    while(i < 10):
        camera.capture('image{0:04d}.jpg'.format(i))     # <<<< Take and save 10 pictures
        i += 1
    b.set_light(21, 'bri', 2)                            # <<<< Take off the flash light after taking pictures

    # ---------------------
    # Save all light status
    # ---------------------

    h4 = b.get_light(4, 'hue')
    h8 = b.get_light(8, 'hue')
    h20 = b.get_light(20, 'hue')
    h22 = b.get_light(22, 'hue')

    br4 = b.get_light(4, 'bri')
    br8 = b.get_light(8, 'bri')
    br20 = b.get_light(20, 'bri')
    br22 = b.get_light(22, 'bri')

    p4 = b.get_light(4, 'on')
    p8 = b.get_light(8, 'on')
    p20 = b.get_light(20, 'on')
    p22 = b.get_light(22, 'on')

    # ---------------------
    # Flash 2 times in GREEN
    # ---------------------

    flash_green()
    execfile("/home/pi/ledon.py")
    flash_green()

    # ---------------------
    # Put back all light status
    # ---------------------

    b.set_light(4,'hue',h4)
    b.set_light(8,'hue',h8)
    b.set_light(20,'hue',h20)
    b.set_light(21,'hue',h21)
    b.set_light(22,'hue',h22)

    b.set_light(4,'bri',br4)
    b.set_light(8,'bri',br8)
    b.set_light(20,'bri',br20)
    b.set_light(21,'bri',br21)
    b.set_light(22,'bri',br22)

    b.set_light(4,'on',p4)
    b.set_light(8,'on',p8)
    b.set_light(20,'on',p20)
    b.set_light(21,'on',p21)
    b.set_light(22,'on',p22)


    execfile("/home/pi/Pi-Tweeter/tweetin.py") # << We already save 10 pictures, now we need to tweet it like a GIF
    time.sleep(7)                              # << This sleep is using to signal cat_out cannot be catch 2 times


import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

a = 0

# -----------------------
# INFINITE LOOP TO CATCH SIGNAL FROM THE GYROSCOPE AND CALL THE GOOD FUNCTION
# -----------------------

while 1:

    # -------------------------------------
    # THIS IS CALCUL TO GET Y AND X ROTATION OF GYROSCOPE
    # -------------------------------------

    def read_byte(reg):
        return bus.read_byte_data(address, reg)

    def read_word(reg):
        h = bus.read_byte_data(address, reg)
        l = bus.read_byte_data(address, reg+1)
        value = (h << 8) + l
        return value

    def read_word_2c(reg):
        val = read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)


    bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
    address = 0x68       # via i2cdetect
    bus.write_byte_data(address, power_mgmt_1, 0)
    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)

    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)

    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

    p21 = b.get_light(21, 'on')
    br21 = b.get_light(21, 'bri')
    h21 = b.get_light(21, 'hue')

    i = 0
    if get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert) > 35:
        print "Sortie du chat !"
        cat_out()
    if get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert) < -35:
        print "Entree du chat !"
        cat_in()
