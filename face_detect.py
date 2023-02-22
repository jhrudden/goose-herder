import cv2

MAC_M1_FOCAL_LENGTH = 50.0  # in millimeters
JH_FACE_HEIGHT = 209.55 # in millimeters

# Referenced: https://photo.stackexchange.com/questions/12434/how-do-i-calculate-the-distance-of-an-object-in-a-photo
def calculate_distance(image_height: float, known_object_height: float, current_height: float, focal_length: float = MAC_M1_FOCAL_LENGTH ) -> float:
    return (focal_length * known_object_height) / current_height


class FaceDetector:
    def __init__(self):
        # setup face classifier
        face_cascade_path = 'data/haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier()
        if not self.face_cascade.load(face_cascade_path):
            print(f"Failed to open haarcascade file: {face_cascade_path}")
            exit(0)
    
    def draw_face_distance(self, frame, face):
        (x, y, w, h) = face
        face_height_in_frame = abs(y - h)
        print(f'height camera {face_height_in_frame}')
        img_height = frame.shape[0]
        dist = calculate_distance(img_height, JH_FACE_HEIGHT, face_height_in_frame)
        dist_ft = int(dist * 0.00328084)
        return cv2.putText(frame, f'{str(dist_ft)}ft', [x + (w // 2), y + (h // 2)], cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 0, 0), 2, cv2.LINE_AA)
        
    def draw_faces(self, frame, faces):
        for face in faces:
            (x, y, w, h) = face
            center = (x + w//2, y + h//2)
            frame = cv2.rectangle(frame, [x, y], [x+w, y+h], (255, 0, 0), 2)
            frame = self.draw_face_distance(frame, face)
        return frame

    def detect_faces(self, frame):
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_grey = cv2.equalizeHist(frame_grey)

        faces = self.face_cascade.detectMultiScale(frame_grey)
        print(faces)
        return faces

    def detect_and_draw(self, frame):
        faces = self.detect_faces(frame)
        return self.draw_faces(frame, faces)



if __name__ == '__main__':

    fd = FaceDetector()
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened:
        print('No current camera detected')
        exit(0)

    while True:
        ret, frame = video_capture.read()
        fd.detect_and_draw(frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        cv2.imshow('frame', frame)
