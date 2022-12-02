from lib.helper_functions import *
from lib.controller_input import XboxController
from lib.tellopic import setup_field
from guizero import App, Text, Combo, Picture
from djitellopy import Tello
from threading import Thread, Lock

# noinspection PyArgumentEqualDefault
app = App(title="Daedalus Robotics Tello GUI", layout="auto")
controller = XboxController()
tello = Tello()
field = setup_field(app=app)
# print(field)


# Button Variables
mp = -1
battery = -1

mission_pad_text = Text(
    app,
    text=f"MP: {mp}",
    align="top"
)

battery_text = Text(
    app,
    text=f"Battery: {battery}%",
    align="top"
)

autonomous_text = Text(
    app,
    text=f"Autonomous Mode: {is_auton}",
    align="top"
)

side_switch = Combo(
    app,
    options=["textron", "residential"],
    selected="textron",
    command=set_side,
    align="top"
)

mission_text = Text(app, text=f"mission: {m_type}")

mission_picture_1 = Picture(
    app,
    image=r"assets\mission_1.png",
    width=778,
    height=296,
    align="left",
    visible=False
)

mission_picture_2 = Picture(
    app,
    image=r"assets\mission_2.png",
    width=778,
    height=296,
    align="left",
    visible=False
)

mission_picture_3 = Picture(
    app,
    image=r"assets\mission_3.png",
    width=778,
    height=296,
    align="left",
    visible=False
)

# noinspection PyArgumentEqualDefault
base_pads_picture = Picture(
    app,
    image=r"assets\basepads.png",
    width=778,
    height=296,
    align="left",
    visible=True
)


tello_lock = Lock()

tello_control_thread = Thread(
    target=lambda: tello_control_loop(
        tello,
        controller,
        tello_lock,
        base_pads_picture,
        field=field
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
        base_pad=base_pads_picture,
        field=field
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
