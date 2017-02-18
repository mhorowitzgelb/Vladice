import time
import picamera
import numpy as np
import cv2

class RaspberryPI:
	camera = picamera.PiCamera()
	buffer_res = (1920, 1088)
	camera_res = (1920, 1080)

	def __init__(self):
		self.camera.resolution = self.camera_res
		# self.camera.framerate = 24
		time.sleep(1)

	def take_picture(self):
		buf_size = self.buffer_res[0] * self.buffer_res[1] * 3
		output = np.empty((buf_size,), dtype=np.uint8)
		self.camera.capture(output, 'bgr')
		output = output.reshape((self.buffer_res[1], self.buffer_res[0], 3))
		return output
	
def show_image(im):
	cv2.namedWindow('im', cv2.WINDOW_NORMAL)
	cv2.imshow('im', im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	print('Taking picture...')
	pi = RaspberryPI()
	im = pi.take_picture()
	show_image(im)
