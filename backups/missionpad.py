from guizero import Picture

# Relic of a different time; no longer used
class MissionPad:

    def __init__(self, mid: int, on_pad: bool, app: App):
        self.mid = mid
        self.on_pad = on_pad
        self.tello = Picture(
            app,
            image=r"assets\tello.png",
            width=100,
            height=100,
            visible=False
        )

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