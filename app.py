from djitellopy import Tello

class TelloController: 
    def __init__(self):
        tello = Tello()

        tello.connect()
        tello.takeoff()

        tello.move_left(100)
        tello.rotate_counter_clockwise(90)
        tello.move_forward(100)

        tello.land()

