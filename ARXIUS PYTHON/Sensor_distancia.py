import RPi.GPIO as GPIO
import time

TRIG = 17

ECO = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECO, GPIO.IN)

while True:

    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(TRIG, GPIO.LOW)
    while GPIO.input(ECO) == 0:
    pulse start = time.time()

    while GPIQ.input(ECHO) == 1:
    pulse_end = time.time()
    durada = pulse end - pulse start
    DURACION = pulseln(ECO, HIGH);
    distancia = durada / 58.2
    print(distancia)
    time.sleep(1)