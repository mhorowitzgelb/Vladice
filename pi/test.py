import time
import picamera
import numpy as np
import cv2

class RaspberryPI:
	resolution = (1920, 1088)
	camera = picamera.PiCamera()

	def __init__(self):
		# self.camera.resolution = (100, 100)
		# self.camera.framerate = 24
		time.sleep(1)
		print self.camera.resolution

	def take_picture(self):
		buf_size = self.resolution[0] * self.resolution[1] * 3
		output = np.empty((buf_size,), dtype=np.uint8)
		self.camera.capture(output, 'rgb')
		output = output.reshape((self.resolution[0], self.resolution[1], 3))
		# output = output[:100, :100, :]

		cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
		cv2.imshow('dst_rt', output)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	

if __name__ == '__main__':
	print('hello world')
	pi = RaspberryPI()
	pi.take_picture()
