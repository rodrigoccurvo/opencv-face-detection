from .multicamera import MultiCamera


class MultiCameraCached(MultiCamera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clear_cache()

    def clear_cache(self):
        self.cams_cache = [None] * len(self)

    def read(self, index):
        if self.cams_cache[index] is None:
            self.cams_cache[index] = super().read(index)

        return self.cams_cache[index]
