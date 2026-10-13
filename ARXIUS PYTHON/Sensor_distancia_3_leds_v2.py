import RPi.GPIO as GPIO 
import time 
# Configuració dels pins 
GPIO.setmode(GPIO.BCM) 
LED1 = 22
LED2 = 23
LED3 = 24
TRIG = 17  # Pin de Trigger 
ECHO = 18  # Pin d'Echo 
GPIO.setup(TRIG, GPIO.OUT) 
GPIO.setup([LED1, LED2, LED3], GPIO.OUT) 
GPIO.setup(ECHO, GPIO.IN) 

def mesura_distancia(): 
# Enviament del pols de Trigger 
    GPIO.output(TRIG, True) 
    time.sleep(0.00001)  # Pols de 10 microsegons 
    GPIO.output(TRIG, False) 
    # Mesura del temps de resposta d'Echo 
    
    inici = time.time()

    while GPIO.input(ECHO) == 0: 
        if time.time() - inici > 0.03:
            return -1
        start_time = time.time() 

    while GPIO.input(ECHO) == 1: 
        if time.time() - start_time > 0.03:
            return -1
        end_time = time.time() 
    
    # Càlcul de la distància 
    temps_total = end_time - start_time 
    distancia = (temps_total * 34300) / 2  # Resultat en cm 
    
    return distancia 
 
try: 
    while True: 
        distancia = mesura_distancia() 
        
        #Entre 0 i 20 cm Led 1 encés i resta apagats
        if 0.1 <= distancia <= 20: #if distancia >=0 and distancia<=0
            GPIO.output(LED1,1)
            GPIO.output(LED2,0)
            GPIO.output(LED3,0)
        #Entre 20 i 50 cm Led 2 encés i resta apagatas
        if 20 < distancia <= 50: #if distancia >20 and distancia<=50
            GPIO.output(LED1,0)
            GPIO.output(LED2,1)
            GPIO.output(LED3,0)
        #Entre 50 i 400 cm Led 3 encés i resta apagatas
        if 50 < distancia <= 400: #if distancia >50 and distancia<=400
            GPIO.output(LED1,0)
            GPIO.output(LED2,0)
            GPIO.output(LED3,1)
        #Qualsevol altre valor els 3 leds encesos com a alarma
        if distancia > 400:
            GPIO.output(LED1,1)
            GPIO.output(LED2,1)
            GPIO.output(LED3,1) 
        if distancia < 0 :
            GPIO.output(LED1,1)
            GPIO.output(LED2,1)
            GPIO.output(LED3,1)
            time.sleep(0.01) 
            GPIO.output(LED1,0)
            GPIO.output(LED2,0)
            GPIO.output(LED3,0)       
            time.sleep(0.01)

    
        print(f"Distancia: {distancia:.2f} cm") 
        time.sleep(1) 
 
except KeyboardInterrupt: 
    print("Mesura aturada per l'usuari") 
    GPIO.cleanup()