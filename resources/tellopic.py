class MissionPad(object):

    def __init__(self, id: int, on_pad: bool):
        self.id = id
        self.on_pad = on_pad

    def set_pad(self, id: int):
        self.id = id

    def get_pad(self):
        return self.id

    def now_on_pad(self):
        self.on_pad = True
        return self.on_pad

    def now_off_pad(self):
        self.on_pad = False
        return self.on_pad
