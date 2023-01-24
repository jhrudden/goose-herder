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

    def handle_key(self, key: int):
        '''Move tello drone based on input key'''
        if key == ord('w'):
            self.tello.move_forward(30)
        elif key == ord('s'):
            self.tello.move_back(30)
        elif key == ord('a'):
            self.tello.move_left(30)
        elif key == ord('d'):
            self.tello.move_right(30)
        elif key == ord('e'):
            self.tello.rotate_clockwise(30)
        elif key == ord('q'):
            self.tello.rotate_counter_clockwise(30)


    def end(self):
        self.tello.streamoff()
    


if __name__ == "__main__":
    tc = TelloController()
    tc.run()

