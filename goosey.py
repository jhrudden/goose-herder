from tello_controller import TelloController
import cv2

TELLO_FOCAL_LENGTH = 3.0


if __name__ == '__main__':
    tc = TelloController()
    tc.run()
