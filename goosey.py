from tello_controller import TelloController 
import cv2

tc = TelloController()
cv2.startWindowThread()

frame_reader = tc.start_stream();
while(True):
    img = frame_reader.frame

    img = cv2.resize(img, (1920, 1080))
    cv2.imshow('Image', img)

    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
tc.end()
cv2.destroyAllWindows()
