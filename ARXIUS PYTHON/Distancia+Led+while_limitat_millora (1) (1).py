import RPi.GPIO as GPIO
import time

LED1 = 12
LED2 = 13
LED3 = 16
TRIG = 17
ECHO = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def echo_timeout(estat):
    inici = time.time()

    while GPIO.input(ECHO) == estat:
        if time.time() - inici > 0.03:
            return True

    return False
    

def mesura_distancia():

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Esperem que ECHO passi de 0 a 1
    if echo_timeout(0):
        return -1

    start_time = time.time()

    # Esperem que ECHO passi de 1 a 0
    if echo_timeout(1):
        return -1

    end_time = time.time()

    temps_total = end_time - start_time
    distancia = (temps_total * 34300) / 2

    return distancia
def llums(distancia):

    if 0 <= distancia <= 20:
        GPIO.output(LED1, 1)
        GPIO.output(LED2, 0)
        GPIO.output(LED3, 0)

    elif distancia <= 50:
        GPIO.output(LED1, 0)
        GPIO.output(LED2, 1)
        GPIO.output(LED3, 0)

    elif distancia <= 400:
        GPIO.output(LED1, 0)
        GPIO.output(LED2, 0)
        GPIO.output(LED3, 1)

    else:
        GPIO.output(LED1, 1)
        GPIO.output(LED2, 1)
        GPIO.output(LED3, 1)

try:

    while True:

        distancia = mesura_distancia()

     
        if distancia != -1:

            print("Distància:", distancia, "cm")
        else:
            print("Sensor No disponible")
            
        time.sleep(0.1)
        
        llums(distancia)

except KeyboardInterrupt:

    print("\nMesura aturada per usuari")
    GPIO.cleanup()