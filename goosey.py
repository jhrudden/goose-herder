from tello_controller import TelloController 
import cv2

TELLO_FOCAL_LENGTH = 3.0

# Referenced: https://photo.stackexchange.com/questions/12434/how-do-i-calculate-the-distance-of-an-object-in-a-photo
def calculate_distance(image_height: int, known_object_height: float, current_height: int, focal_length: float = MAC_M1_FOCAL_LENGTH ) -> float:
    return (focal_length * image_height * current_height) / known_object_height


if __name__ == '__main__':
    tc = TelloController()
    tc.run()
