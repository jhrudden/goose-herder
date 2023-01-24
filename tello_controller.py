from djitellopy import Tello




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
    


if __name__ == "__main__":
    tc = TelloController()
    tc.run()

