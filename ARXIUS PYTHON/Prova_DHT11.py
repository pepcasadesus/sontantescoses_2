import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import sys

sensor = 11

pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([sensor,pin], GPIO.IN)
#GPIO.setup(ECHO, GPIO.IN)
#GPIO.output([RS,E,D4,D5,D6,D7], 0)

# Senyal compartit per indicar als fils que han de parar
#aturar = threading.Event()



# --------------------------------------------------
# Programa principal
# --------------------------------------------------

try:
    comptador = 1
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity is not None and temperature is not None:
            print(f'Temp={temperature:.2f}*  Humidity={humidity:.2f}%')

            #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            # 2. Corregida la concatenació de text i números
            if comptador == 1:
                print(f"{comptador} cop mesurat")
            else:
                print(f"{comptador} cops mesurats")
            # Incrementem el comptador correctament abans o després de comprovar
            comptador += 1  
        else:

            print('Impossible llegir. Prova un altre cop!')

    
        time.sleep(1)

except KeyboardInterrupt:

    print("Aturant programa...")

    #aturar.set()

    #fil_1.join()
    #fil_2.join()

    GPIO.cleanup()

    print("Programa finalitzat")
    sys.exit(1)