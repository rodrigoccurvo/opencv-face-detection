# Code inspired by:
# https://arcoresearchgroup.wordpress.com/2020/06/02/virtual-camera-for-opencv-using-v4l2loopback/
# TODO: check https://pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

import cv2
import time


ESC = 27


def window_closed(window_title):
    key_pressed = cv2.waitKey(1)

    try:
        window_closed = not cv2.getWindowProperty(
            window_title, cv2.WND_PROP_VISIBLE)
    except cv2.error:
        window_closed = False

    return key_pressed == ESC or window_closed


CAM_DEVICE = "/dev/video0"
WIDTH, HEIGHT = 800, 450


def open_cam():
    cam = cv2.VideoCapture(CAM_DEVICE)

    assert cam.isOpened()

    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    return cam


WINDOW_TITLE = "Preview"

FRAME_RATE = 30
FRAME_DELAY = 1.0 / FRAME_RATE


def main():
    cam = open_cam()

    last_time = 0

    while not window_closed(WINDOW_TITLE):
        if time.time() - last_time >= FRAME_DELAY:
            has_frame, cam_img = cam.read()

            if has_frame:
                cv2.imshow(WINDOW_TITLE, cam_img)

            last_time = time.time()
        else:
            cam.grab()

    cv2.destroyAllWindows()
    cam.release()


if __name__ == "__main__":
    print("Running...")
    main()
