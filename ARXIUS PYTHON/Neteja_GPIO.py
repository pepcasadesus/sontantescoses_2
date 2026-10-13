import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([17,25], GPIO.OUT)
for pin in [17,25]:
    GPIO.output(pin, GPIO.OUT)
#GPIO.output(25, GPIO.OUT)
GPIO.cleanup
