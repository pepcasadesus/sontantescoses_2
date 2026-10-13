#Hem de fer tots els previs: IMPORT / PIN DE RASPBERRY MODE BCM/ PINS DE SORTIDA
# Previs
import RPi.GPIO as GPIO
import time

led1 = 17
led2 = 25
pausa = 0.5

def estat(estat1, estat2, delay):
	GPIO.output(led1,estat1)
	GPIO.output(led2, estat2)
	time.sleep(delay)

GPIO.setmode(GPIO.BCM) # per definir el sistema que anomenarem els pins
GPIO.setup([led1,led2], GPIO.OUT)

# Execució
while True:
	# Posem les sortides amb el valor que volem, encès o apagat
	estat(GPIO.HIGH, GPIO.LOW, pausa)
	estat(GPIO.LOW, GPIO.HIGH, pausa)