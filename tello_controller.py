from djitellopy import Tello
import pygame
import cv2
import numpy as np
import time

# CONSTANTS
DRONE_SPEED = 60
FPS = 80

class TelloController: 
    """Creates a display of tello video stream and moves drone via key events
       Escape key -> quits
       Controls:
          - T: 
          - L: Land
          - Arrow keys: Forward, backward, left and right.
          - A and D: Counter clockwise and clockwise rotations (yaw)
          - W and S: Up and down.
    """
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("There is a goose on the loose")
        self.screen = pygame.display.set_mode([960, 720])

        self.tello = Tello()


        #######
        # MOVEMENT VELOCITIES
        #######
        self.z_v = 0 # forward & back
        self.x_v = 0 # left & right
        self.y_v = 0 # up & down
        self.yaw_v = 0 # twisting

        self.send_rc_control = False

        # Only send controls to drone once per 1000 // FPS millis
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):
        self.tello.connect()
        self.tello.set_speed(DRONE_SPEED)

        # Ensure drone isn't still streaming from quiting without ending it
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle keydown
                    raise NotImplementedError()
                elif event.type == pygame.KEYUP:
                    # Handle keyup
                    raise NotImplementedError()
            
            # Ensure no issue has occurred with video stream from drone
            if frame_read.stopped:
                break
            
            self.screen.fill([0,0,0])
            
            frame = frame_read.frame

            # display battery on screen
            text = f"Battery: {self.tello.get_battery()}%"
            cv2.putText(frame, text, (5, 720-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 176, 79), 2)
            # TODO: Figure this out
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)

            self.screen.blit(frame, (0,0))

            time.sleep(1 / FPS)

        self.tello.end()

    def update(self):
        """ Send velocities to tello """

        if self.send_rc_control:
            self.tello.send_rc_control(self.x_v, self.z_v, self.y_v, self.yaw_v)




    def start_stream(self):
        '''Turns on tello stream settings and returns frame stream'''
        self.tello.streamon()
        return self.tello.get_frame_read()


    def end(self):
        self.tello.land()
        self.tello.streamoff()
    


if __name__ == "__main__":
    tc = TelloController()
    tc.run()

