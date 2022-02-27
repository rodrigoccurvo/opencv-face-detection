import cv2


def open_cam(device, resolution):
    cam = cv2.VideoCapture(device)

    if not cam.isOpened():
        raise SystemExit(f"Unable to open {device}")

    width, height = resolution
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cam


class Camera(cv2.VideoCapture):
    def __init__(self, device, resolution):
        super().__init__(device)

        if not self.isOpened():
            raise SystemExit(f"Unable to open {device}")

        width, height = resolution
        self.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


