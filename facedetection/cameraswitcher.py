from .camera import Camera


class CameraSwitcher:
    def __init__(self, devices, resolution):
        self.devices = devices
        self.resolution = resolution

        self.cams = [
            Camera(device, self.resolution)
            for device in self.devices
        ]

        self.previous = 0
        self.current = 0

    def select(self, index):
        if index == self.current:
            return False

        try:
            # Check if camera exists, otherwise it raises an IndexError
            self.cams[index]

            self.previous = self.current
            self.current = index
        except IndexError:
            return False
        else:
            return True

    def read(self):
        return self.cams[self.current].read()

    def flush(self):
        # Grab frame without processing it, just to empty buffer
        for cam in self.cams:
            cam.grab()

    def release(self):
        for cam in self.cams:
            cam.release()



