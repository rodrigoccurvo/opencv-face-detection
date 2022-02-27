# Code inspired by:
# https://arcoresearchgroup.wordpress.com/2020/06/02/virtual-camera-for-opencv-using-v4l2loopback/
# TODO: check https://pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

import cv2
import time

from facedetection.facedetection import FaceDetector, CachedFaceDetector
from facedetection.camera import Camera
from facedetection.cameraswitcher import CameraSwitcher
from facedetection.fadecameraswitcher import FadeCameraSwitcher
from facedetection.autocameraswitcher import AutoCameraSwitcher


ESC = 27
NUM_KEYS = [ord(str(i)) for i in range(10)]


def window_closed(window_title):
    try:
        window_closed = not cv2.getWindowProperty(
            window_title, cv2.WND_PROP_VISIBLE)
    except cv2.error:
        window_closed = False

    return window_closed


WINDOW_TITLE = "Preview"

FRAME_RATE = 30
FRAME_DELAY = 1.0 / FRAME_RATE


def main():

    camswitcher = AutoCameraSwitcher(
        devices=["/dev/video2", "/dev/video0"], resolution=(640, 480))
    detector = FaceDetector()

    last_time = 0

    while not window_closed(WINDOW_TITLE):
        if time.time() - last_time >= FRAME_DELAY:
            last_time = time.time()
            has_frame, cam_img = camswitcher.read()
            if not has_frame:
                continue

            detector.find_faces(cam_img)

            cv2.imshow(WINDOW_TITLE, cam_img)

        else:
            # Flush buffer
            camswitcher.flush()

        key_pressed = cv2.waitKey(1)

        if key_pressed in NUM_KEYS:
            num_pressed = int(chr(key_pressed))
            if camswitcher.select(num_pressed - 1):
                print(f"Selected camera {num_pressed}")
            else:
                print(f"Can't select camera {num_pressed}")
        elif key_pressed == ESC:
            break

    cv2.destroyAllWindows()
    camswitcher.release()


if __name__ == "__main__":
    print("Running...")
    main()
