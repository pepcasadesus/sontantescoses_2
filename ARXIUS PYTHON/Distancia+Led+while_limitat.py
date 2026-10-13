import RPi.GPIO as GPIO
import time

LED1 = 22
LED2 = 23
LED3 = 24
TRIG = 17
ECHO = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def mesura_distancia():

    GPIO.output(TRIG, True)
    time.sleep(0.00001) #10 us  ----- 30000 us
    GPIO.output(TRIG, False)

    # Esperem que ECHO passi de 0 a 1
    inici = time.time()

    while GPIO.input(ECHO) == 0:

        if time.time() - inici > 0.03:
            return -1

        start_time = time.time()

    # Esperem que ECHO torni de 1 a 0
    while GPIO.input(ECHO) == 1:

        if time.time() - start_time > 0.03:
            return -1

        end_time = time.time()

    temps_total = end_time - start_time
    distancia = (temps_total * 34300) / 2

    return distancia


def llums(distancia):

    if 0.1 <= distancia <= 20:
        GPIO.output(LED1, 1)
        GPIO.output(LED2, 0)
        GPIO.output(LED3, 0)

    if 20 < distancia <= 50:
        GPIO.output(LED1, 0)
        GPIO.output(LED2, 1)
        GPIO.output(LED3, 0)

    if 50 < distancia <= 400:
        GPIO.output(LED1, 0)
        GPIO.output(LED2, 0)
        GPIO.output(LED3, 1)

    if distancia > 400:
        GPIO.output(LED1, 1)
        GPIO.output(LED2, 1)
        GPIO.output(LED3, 1)

    if distancia < 0:
        GPIO.output(LED1, 0)
        GPIO.output(LED2, 0)
        GPIO.output(LED3, 0)
        time.sleep(0.01)
        GPIO.output(LED1, 1)
        GPIO.output(LED2, 1)
        GPIO.output(LED3, 1)
        time.sleep(0.01)

try:

    while True:

        distancia = mesura_distancia()

        llums(distancia)

        print("Distància:", distancia, "cm")

        time.sleep(0.1)

except KeyboardInterrupt:

    print("\nMesura aturada per usuari")
    GPIO.cleanup()