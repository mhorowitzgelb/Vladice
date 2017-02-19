"""
Main program for the Raspberry PI robot.

"""
from button import wait_for_button
from bot import RaspberryPI
from ai import ai_move
import time
from homography import run_homography

def run():
		pi = RaspberryPI()

		# Find corners of the game board and compute homography
		while True:
			# Wait for button press
			wait_for_button()

			# Wait  200ms, then take picture of board
			im = pi.take_picture()

			# Parse image to create board
			board = run_homography(im)

			# Determine AI move
			move = ai_move(board)

			# Announce AI move on the speakers, and print it to console
			pi.voice_position(move[0],move[1])

if __name__ == '__main__':
	run()
