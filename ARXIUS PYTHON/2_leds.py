#Hem de fer tots els previs: IMPORT / PIN DE RASPBERRY MODE BCM/ PINS DE SORTIDA
# Previs
import RPi.GPIO as GPIO
import time
# Si només volem importar un dels mòduls (p.e sleep faríem FROM TIME IMPORT SLEEP)
# Aleshores podem escriure directament sleep(1)
GPIO.setmode(GPIO.BCM) # per definir el sistema que anomenarem els pins
GPIO.setup([17,25], GPIO.OUT)
# Execució
while True:
	# Posem les sortides amb el valor que volem, encès o apagat
	GPIO.output(17,GPIO.HIGH)
	GPIO.output(25,GPIO.LOW)
	time.sleep(0.5)  
# Estaran amb aquests valors el temps de dins del parèntesi
# Posem les sortides amb el valor que volem, encès o apagat
	GPIO.output(17,GPIO.LOW)
	GPIO.output(25,GPIO.HIGH)
	time.sleep(0.5) 
# Estaran amb aquests valors el temps de dins del parèntesi