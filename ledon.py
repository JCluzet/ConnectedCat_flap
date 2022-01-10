#!/usr/bin/env python
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

LED = 11 #Définit le numéro du port GPIO qui alimente la led
LEDOFF = 12

GPIO.setup(LED, GPIO.OUT) #Active le contrôle du GPIO
GPIO.setup(LEDOFF, GPIO.OUT)
#state = GPIO.input(LED) #Lit l'état actuel du gpio, vrai si allumé, faux si éteint
state = GPIO.input(LEDOFF) #Lit l'état actuel du GPIO, vrai si allumé, faux si éteint

if state : #Si GPIO allumé
    GPIO.output(LEDOFF, GPIO.LOW) #On l’éteint

state = GPIO.input(LED)
if not state : 
    GPIO.output(LED, GPIO.HIGH) #On l'allume
