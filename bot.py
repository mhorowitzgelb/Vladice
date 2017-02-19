import time
import picamera
import numpy as np
import cv2
from subprocess import call
import pyttsx

class RaspberryPI:
	camera = picamera.PiCamera()
	buffer_res = (1920, 1088)
	camera_res = (1920, 1080)

	def __init__(self):
		self.camera.resolution = self.camera_res
		# self.camera.framerate = 24
		# time.sleep(1)

	def take_picture(self):
		buf_size = self.buffer_res[0] * self.buffer_res[1] * 3
		output = np.empty((buf_size,), dtype=np.uint8)
		self.camera.capture(output, 'bgr')
		output = output.reshape((self.buffer_res[1], self.buffer_res[0], 3))
		return output

	def voice_tile(self):
		pass

	def voice(self, line):
		engine = pyttsx.init()
		engine.setProperty('rate', 70)
		voices = engine.getProperty('voices')
		best_voice = voices[2]
		engine.setProperty('voice', best_voice.id)
		engine.say(line)
		engine.runAndWait()

	def voice_position(self, row, col):
		rows = [
			'a','bee','cee','dee','ee','ef','gee','h','i','j','k'
		]
		cols = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven']
		self.voice('My move is' + ',' + rows[row] + ',' + cols[col])


def show_image(im):
	cv2.imshow('im', im)
	cv2.waitKey(10)

if __name__ == '__main__':
	pi = RaspberryPI()
	cv2.namedWindow('im', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('im', 960, 540)
	while True:
		im = pi.take_picture()
		show_image(im)
	cv2.destroyAllWindows()
	# pi.voice('what is my purpose')

