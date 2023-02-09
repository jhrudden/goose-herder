import cv2


def detect_face(frame):
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_grey = cv2.equalizeHist(frame_grey)

    faces = face_cascade.detectMultiScale(frame_grey)
    for (x, y, w, h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv2.rectangle(frame, [x, y], [x+w, y+h], (255, 0, 0), 2)
    cv2.imshow('frame', frame)


if __name__ == '__main__':

    # setup face classifier
    face_cascade_path = 'data/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(face_cascade_path):
        print(f"Failed to open haarcascade file: {face_cascade_path}")
        exit(0)

    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened:
        print('No current camera detected')
        exit(0)

    while True:
        ret, frame = video_capture.read()
        detect_face(frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
