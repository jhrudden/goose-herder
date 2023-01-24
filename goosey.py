from tello_controller import TelloController 
import cv2

tc = TelloController()
cv2.startWindowThread()

frame_reader = tc.start_stream();
while(True):
    img = frame_reader.frame

    img = cv2.resize(img, (1920, 1080))
    cv2.imshow('Image', img)

    # Handle key press
    key = cv2.waitKey(1) & 0xFF
    

    if key == ord('q'):
        break
    
    # Control tello with keyboard
    tc.handle_key(key)

tc.end()
cv2.destroyAllWindows()
