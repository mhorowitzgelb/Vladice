import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button():
	while True:
	    input_state = GPIO.input(18)
	    if input_state == False:
		time.sleep(0.5)
		return

