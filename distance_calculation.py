
MAC_M1_FOCAL_LENGTH = 50.0  # in millimeters
TELLO_FOCAL_LENGTH = 3.0

# Referenced: https://photo.stackexchange.com/questions/12434/how-do-i-calculate-the-distance-of-an-object-in-a-photo


def calculate_distance(focal_length: float, image_height: int, known_object_height: float, current_height: int) -> float:
    return (focal_length * image_height * current_height) / known_object_height
