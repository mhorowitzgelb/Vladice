"""
Main program for the Raspberry PI robot.

"""
from button import wait_for_button
import RPi.GPIO as GPIO
import time

def run():
		# Find corners of the game board and compute homography
		while True:
			# Wait for button press
			wait_for_button()
			print 'done'
			# Wait  200ms, then take picture of board
			# Parse image to create board
			# Determine AI move
			# Announce AI move on the speakers, and print it to console

if __name__ == '__main__':
	run()
