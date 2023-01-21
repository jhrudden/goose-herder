from djitellopy import Tello
import cv2
import imutils




class TelloController: 
    tello = None;
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
    
    def start_stream(self):
        '''Turns on tello stream settings and returns frame stream'''
        self.tello.streamon()
        return self.tello.get_frame_read()

    def end(self):
        self.tello.streamoff()

    def run_stream(self):
        cv2.startWindowThread()
        frame_reader = self.start_stream();
        while(True):
            img = frame_reader.frame

            img = cv2.resize(img, (1920, 1080))
            cv2.imshow('Image', img)

            if cv2.waitKey(1)& 0xFF == ord('q'):
                break
        self.end()
        cv2.destroyAllWindows()


TelloController().run_stream()
