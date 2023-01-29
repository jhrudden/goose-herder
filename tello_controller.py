from djitellopy import Tello
import pygame
import cv2
import numpy as np
import time

# CONSTANTS
DRONE_SPEED = 60
FPS = 120


class TelloController: 
    """Creates a display of tello video stream and moves drone via key events
       Escape key -> quits
       Controls:
          - T: Takeoff
          - L: Land
          - Arrow keys: Forward, backward, left and right.
          - A and D: Counter clockwise and clockwise rotations (yaw)
          - W and S: Up and down.

        # Reference: https://github.com/damiafuentes/DJITelloPy/blob/master/examples/manual-control-pygame.py

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
                    if event.type == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    # Handle keyup
                    self.keyup(event.key)
            
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

            pygame.display.update()

            time.sleep(1 / FPS)

        self.tello.end()

    def update(self):
        """ Send velocities to tello """

        if self.send_rc_control:
            self.tello.send_rc_control(self.x_v, self.z_v, self.y_v, self.yaw_v)

    def keydown(self, key):
            """ Update velocities based on key pressed
            Arguments:
                key: pygame key
            """
            if key == pygame.K_UP:  # set forward velocity
                self.z_v = DRONE_SPEED
            elif key == pygame.K_DOWN:  # set backward velocity
                self.z_v = -DRONE_SPEED
            elif key == pygame.K_LEFT:  # set left velocity
                self.x_v = -DRONE_SPEED
            elif key == pygame.K_RIGHT:  # set right velocity
                self.x_v = DRONE_SPEED
            elif key == pygame.K_w:  # set up velocity
                self.y_v = DRONE_SPEED
            elif key == pygame.K_s:  # set down velocity
                self.y_v = -DRONE_SPEED
            elif key == pygame.K_a:  # set yaw counter clockwise velocity
                self.yaw_v = -DRONE_SPEED
            elif key == pygame.K_d:  # set yaw clockwise velocity
                self.yaw_v = DRONE_SPEED

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.z_v = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.x_v = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.y_v = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_v = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False


    def start_stream(self):
        '''Turns on tello stream settings and returns frame stream'''
        self.tello.streamon()
        return self.tello.get_frame_read()


if __name__ == "__main__":
    tc = TelloController()
    tc.run()

