import numpy as np
from guizero import Picture, App, Box


class MissionPad:

    def __init__(self, mid: int, on_pad: bool, app: App):
        self.mid = mid
        self.on_pad = on_pad
        self.tello = Picture(app, )

    @property
    def pad(self) -> int:
        return self.mid

    @pad.setter
    def pad(self, mid: int) -> None:
        self.mid = mid

    def now_on_pad(self):
        self.on_pad = True
        return self.on_pad

    def now_off_pad(self):
        self.on_pad = False
        return self.on_pad


def setup_field_textron() -> np.ndarray:
    field = np.ndarray(shape=(2, 4), dtype=MissionPad)
    pads = np.array([7, 1, 3, 5, 8, 2, 4, 6]).reshape(2, 4)

    for row in range(2):
        for col in range(4):
            field[row, col] = MissionPad(pads[row, col], False)

    return field
