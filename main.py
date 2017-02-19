"""
Main program for the Raspberry PI robot.

"""
from button import wait_for_button
from bot import RaspberryPI
from ai import ai_move
import RPi.GPIO as GPIO
import time

def run():
		pi = RaspberryPI()
		# Find corners of the game board and compute homography
		while True:
			pi.voice('i yearn for death')
			# Wait for button press
			wait_for_button()

			# Wait  200ms, then take picture of board
			im = pi.take_picture()

			# Parse image to create board
			board = parse_board(im)

			# Determine AI move
			move = ai_move(board)

			# Announce AI move on the speakers, and print it to console
			pi.voice_position(move[0],move[1])

""" Given a top-down image of the game board, compute a 2d array
where array[row][col] is:
	0 if empty
	1 if player square
	2 if computer square
"""
def parse_board(board_im):
	return []

def ai_move(board):
	return (0,0)

if __name__ == '__main__':
	run()
