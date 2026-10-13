#Dos LEDs amb intervals diferents i multiprocessing
import RPi.GPIO as IO
import time
import multiprocessing
pin_led1 = 17
pin_led2 = 25
IO.setmode(IO.BCM)
IO.setup(pin_led1, IO.OUT)
IO.setup(pin_led2, IO.OUT)
def led1_blink():
	while True:
		IO.output(pin_led1, not IO.input(pin_led1))
		time.sleep(1.5)
def led2_blink():
	while True:
		IO.output(pin_led2, not IO.input(pin_led2))
		time.sleep(1)
#if __name__ == '__main__':
process_1 = multiprocessing.Process(target=led1_blink)
process_2 = multiprocessing.Process(target=led2_blink)
process_1.start()
process_2.start()
process_1.join()
process_2.join()