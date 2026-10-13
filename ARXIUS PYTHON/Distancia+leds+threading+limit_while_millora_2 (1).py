import RPi.GPIO as GPIO
import time
import threading

LED1 = 12
LED2 = 13
LED3 = 16
TRIG = 17
ECHO = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Variable compartida pels dos fils
distancia = 0

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()


# --------------------------------------------------
# Funció auxiliar: comprova si ECHO supera el timeout
# --------------------------------------------------

def echo_timeout(estat):

    inici = time.time()

    while GPIO.input(ECHO) == estat:

        if time.time() - inici > 0.03:
            return True

    return False


# --------------------------------------------------
# FIL 1: mesura la distància
# --------------------------------------------------

def mesura_distancia():

    global distancia

    while not aturar.is_set():

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        if echo_timeout(0):
            distancia = -1

        else:
            start_time = time.time()

            # Esperem que ECHO passi de 1 a 0
            if echo_timeout(1):
                distancia = -1

            else:
                end_time = time.time()

                temps_total = end_time - start_time
                distancia = (temps_total * 34300) / 2

        time.sleep(0.1)
        
        
 
# --------------------------------------------------
# Funció auxiliar per controlar els LEDs
# --------------------------------------------------

def encendre_llums(led1, led2, led3):

    GPIO.output(LED1, led1)
    GPIO.output(LED2, led2)
    GPIO.output(LED3, led3)


# --------------------------------------------------
# FIL 2: controla els LEDs
# --------------------------------------------------

def llums():

    global distancia

    while not aturar.is_set():

        if 0 <= distancia <= 20:
            encendre_llums(1, 0, 0)

        elif distancia <= 50:
            encendre_llums(0, 1, 0)

        elif distancia <= 400:
            encendre_llums(0, 0, 1)

        else:
            encendre_llums(1, 1, 1)

        time.sleep(0.1)


# --------------------------------------------------
# Creació dels fils
# --------------------------------------------------

fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=llums)

fil_1.start()
fil_2.start()


# --------------------------------------------------
# Programa principal
# --------------------------------------------------

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("Aturant programa...")

    aturar.set()

    fil_1.join()
    fil_2.join()

    GPIO.cleanup()

    print("Programa finalitzat")