from .cameraswitcher import CameraSwitcher
import time


class FadeCameraSwitcher(CameraSwitcher):
    def __init__(self, fade_delay=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fade_delay = fade_delay
        self.select_time = 0
        self.current_opacity = 1.0

    def select(self, index):
        # Don't change camera if we're
        # in the middle of a fade
        if self.current_opacity < 1.0:
            return False

        ret = super().select(index)

        if ret:
            self.current_opacity = 0.0
            self.select_time = time.time()

        return ret

    def is_fading(self):
        return self.current_opacity != 1.0

    def _read_cam(self, index):
        return self.cams[index].read()

    def read(self):
        curr_has_frame, curr_img = self._read_cam(self.current)

        if not self.is_fading() or not curr_has_frame:
            return curr_has_frame, curr_img

        prev_has_frame, prev_img = self._read_cam(self.previous)

        if not prev_has_frame:
            return curr_has_frame, curr_img

        blend = curr_img * self.current_opacity
        blend += prev_img * (1 - self.current_opacity)

        self.current_opacity = (time.time() - self.select_time) / self.fade_delay
        self.current_opacity = min(self.current_opacity, 1.0)

        return True, blend.astype(curr_img.dtype)