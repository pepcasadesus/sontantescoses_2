# PROGRAMA PER A CONTROL DE DISTANCIA + PANTALLA LED EN FILS
import RPi.GPIO as GPIO
import time
import threading

TRIG = 20
ECHO = 21
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24
PAUSA = 0.02

ALFABET = {
    "A":(0,0,1,0, 1,0,0,0),
    "B":(0,0,1,0, 0,1,0,0),
    "C":(0,0,1,0, 1,1,0,0),
    "D":(0,0,1,0, 0,0,1,0),
    "E":(0,0,1,0, 1,0,1,0),
    "F":(0,0,1,0, 0,1,1,0),
    "G":(0,0,1,0, 1,1,1,0),
    "H":(0,0,1,0, 0,0,0,1),
    "I":(0,0,1,0, 1,0,0,1),
    "J":(0,0,1,0, 0,1,0,1),
    "K":(0,0,1,0, 1,1,0,1),
    "L":(0,0,1,0, 0,0,1,1),
    "M":(0,0,1,0, 1,0,1,1),
    "N":(0,0,1,0, 0,1,1,1),
    "O":(0,0,1,0, 1,1,1,1),
    "P":(1,0,1,0, 0,0,0,0),
    "Q":(1,0,1,0, 1,0,0,0),
    "R":(1,0,1,0, 0,1,0,0),
    "S":(1,0,1,0, 1,1,0,0),
    "T":(1,0,1,0, 0,0,1,0),
    "U":(1,0,1,0, 1,0,1,0),
    "V":(1,0,1,0, 0,1,1,0),
    "W":(1,0,1,0, 1,1,1,0),
    "X":(1,0,1,0, 0,0,0,1),
    "Y":(1,0,1,0, 1,0,0,1),
    "Z":(1,0,1,0, 0,1,0,1),
    " ":(0,1,0,0, 0,0,0,0),
    ".":(0,1,0,0, 0,1,1,1),
    "0":(1,1,0,0, 0,0,0,0),
    "1":(1,1,0,0, 1,0,0,0),
    "2":(1,1,0,0, 0,1,0,0),
    "3":(1,1,0,0, 1,1,0,0),
    "4":(1,1,0,0, 0,0,1,0),
    "5":(1,1,0,0, 1,0,1,0),
    "6":(1,1,0,0, 0,1,1,0),
    "7":(1,1,0,0, 1,1,1,0),
    "8":(1,1,0,0, 0,0,0,1),
    "9":(1,1,0,0, 1,0,0,1)
    }

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([TRIG,RS,E,D4,D5,D6,D7], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output([RS,E,D4,D5,D6,D7], 0)

# Variable compartida pels dos fils
distancia = 0


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

def lcd():

    global distancia
    comptador = 0
    adistancia = str(distancia)
    for index in range(len(adistancia)):
        if index % 16 == 0:
            if comptador % 2 == 0:
                esborra_la_pantalla()
                escriu_a_fila_u()
            else:
                escriu_a_fila_dos()
            comptador  += 1
        #envia_dades_al_display(ALFABET[distancia[index]])
        envia_dades_al_display(ALFABET[adistancia[index]])
    esborra_la_pantalla()

def modecomandament(valor):
    if valor == False:
         GPIO.output(RS, 1)  
    else:
         GPIO.output(RS,0)
    GPIO.output(E, 0)  
 
def escriu_a_fila_u():
     modecomandament(True)  # El que entrarem sera un comandament
     escriu4bits(0,0,0,0)   # Es posiciona el cursor a l'inici de la filera 1 
     escriu4bits(0,0,0,0)
  
def escriu_a_fila_dos():
     modecomandament(True) # El que entrarem sera un comandament
     escriu4bits(0,0,1,1)  # Es posiciona el cursor a l'inici de la filera 2 
     escriu4bits(0,0,0,0)
              
def escriu4bits(b1,b2,b3,b4):
     GPIO.output(D4, b1)
     GPIO.output(D5, b2)
     GPIO.output(D6, b3)
     GPIO.output(D7, b4)  
     time.sleep(PAUSA)
     GPIO.output(E, 1) 
     GPIO.output(E, 0)       
     time.sleep(PAUSA)
     
def esborra_la_pantalla():
    modecomandament(True)# El que entrarem sera un comandament
    time.sleep(PAUSA)
    escriu4bits(0,0,0,0) # Entrem el primer nibble del comandament esborrar pantalla
    escriu4bits(1,0,0,0) # Entrem el segon nibble del comandament esborrar pantalla
 
def envia_dades_al_display(dada):
    modecomandament(False) # El que entrarem sera un caracter per escriure en pantalla.
    escriu4bits(dada[0],dada[1],dada[2], dada[3]) 
    escriu4bits(dada[4],dada[5], dada[6], dada[7]) 
    #GPIO.output(RS, 0)
    #time.sleep(PAUSA)
  
def detencio_pantalla():
    modecomandament(True)# El que entrarem sera un comandament
    escriu4bits(0,0,0,0) # Entrem el Primer nibble del caracter a detencio_pantalla
    escriu4bits(0,0,1,1) # Entrem el Segon nibble del caracter a detencio_pantalla
   
def inicia_pantalla():
    modecomandament(True) # El que entrarem sera la sequencia d'inicializacio
    for index in range(3):
        escriu4bits(1,1,0,0)
    for index in range(2):
        escriu4bits(0,1,0,0)
    # Canvi a la sequencia inicialitzacio per habilitar dues fileres
    escriu4bits(1,0,1,1)  
    escriu4bits(0,0,0,0)
    escriu4bits(1,1,1,1)
    esborra_la_pantalla()

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
    inicia_pantalla()
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("Aturant programa...")

    aturar.set()

    fil_1.join()
    fil_2.join()

    GPIO.cleanup()

    print("Programa finalitzat")