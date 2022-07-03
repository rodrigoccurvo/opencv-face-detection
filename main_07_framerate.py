import cv2
import time

from facedetection.autocameraswitcher import AutoCameraSwitcher
from facedetection.facedetection import FaceDetector
from facedetection.multicameracached import MultiCameraCached


def window_closed(window_title):
    try:
        window_closed = not cv2.getWindowProperty(
            window_title, cv2.WND_PROP_VISIBLE)
    except cv2.error:
        window_closed = False

    return window_closed


WINDOW_TITLE = "Preview"
ESC = 27
NUM_KEYS = [ord(str(i)) for i in range(10)]

FRAME_RATE = 30
FRAME_DELAY = 1.0 / FRAME_RATE


def main():
    multicam = MultiCameraCached(
        devices=["/dev/video0", "/dev/video2"],
        resolution=(640, 480)
    )
    camswitcher = AutoCameraSwitcher(multicam)
    detector = FaceDetector()

    last_time = 0
    key_pressed = 0

    while not window_closed(WINDOW_TITLE) and key_pressed != ESC:
        if time.time() - last_time >= FRAME_DELAY:
            last_time = time.time()
            multicam.clear_cache()
            has_frame, cam_img = camswitcher.read()

            if not has_frame:
                continue

            detector.find_faces(cam_img)

            cv2.imshow(WINDOW_TITLE, cam_img)
        else:
            # Flush buffer
            multicam.flush()

        key_pressed = cv2.waitKey(1)

        if key_pressed in NUM_KEYS:
            num = int(chr(key_pressed))
            if camswitcher.select(num - 1):
                print(f"Selected camera {num}")
            else:
                print(f"Can't select camera {num}")

    cv2.destroyAllWindows()
    multicam.release()


if __name__ == "__main__":
    print("Running...")
    main()
