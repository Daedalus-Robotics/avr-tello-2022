import PIL.Image

from lib.helper_functions import *
from guizero import App, Text, Combo, Picture, Box
from djitellopy import Tello
from threading import Thread, Lock
from lib.controller_input import XboxController
from PIL import Image

app = App(title="Daedalus Robotics Tello GUI", layout="auto")
controller = XboxController()
tello = Tello()
logo = Image.open(r"assets\logo.png").resize(size=(500, 500))
print(type(logo))
app.image = logo

# Button Variables
mp = -1
battery = -1

mission_pad_text = Text(
    app,
    text=f"MP: {mp}"
)

battery_text = Text(
    app,
    text=f"Battery: {battery}%"
)

autonomous_text = Text(
    app,
    text=f"Autonomous Mode: {is_auton}"
)

side_switch = Combo(
    app,
    options=["textron", "residential"],
    selected="textron",
    command=set_side
)

mission_text = Text(app, text=f"mission: {m_type}")

mission_picture_1 = Picture(
    app,
    image=r"assets\mission_1.png",
    width=778,
    height=296,
    align="bottom",
    visible=False
)

mission_picture_2 = Picture(
    app,
    image=r"assets\mission_2.png",
    width=778,
    height=296,
    align="bottom",
    visible=False
)

mission_picture_3 = Picture(
    app,
    image=r"assets\mission_3.png",
    width=778,
    height=296,
    align="bottom",
    visible=False
)

# noinspection PyArgumentEqualDefault
base_pads_picture = Picture(
    app,
    image=r"assets\basepads.png",
    width=778,
    height=296,
    align="bottom",
    visible=True
)


tello_lock = Lock()

tello_control_thread = Thread(
    target=lambda: tello_control_loop(
        tello,
        controller,
        tello_lock
    ),
    daemon=True
)


tello_update_thread = Thread(
    target=lambda: tello_update_loop(
        tello,
        battery_text,
        mission_pad_text
    ),
    daemon=True
)

tello_status_thread = Thread(
    target=lambda: switch_status(
        tello,
        controller,
        tello_lock,
        autonomous_text,
        mission_text,
        mission_picture_1,
        mission_picture_2,
        mission_picture_3,
        base_pads_picture
    ),
    daemon=True
)

tello.connect()
tello.set_mission_pad_detection_direction(0)

try:
    tello_control_thread.start()
    tello_update_thread.start()
    tello_status_thread.start()
    app.display()
finally:
    tello.end()
