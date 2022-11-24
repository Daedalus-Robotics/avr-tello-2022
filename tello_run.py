from resources.helper_functions import (is_auton, set_side, m_type,
                                        tellocontrolloop, telloupdateloop,
                                        switch_status)
from guizero import App, Text, Combo, Picture
from djitellopy import Tello
from threading import Thread, Lock
from resources.ControllerInput import XboxController

app = App(title="tello-control")
controller = XboxController()
tello = Tello()

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
    image="mission1.png",
    width=450,
    height=300,
    visible=False
)

mission_picture_2 = Picture(
    app,
    image="mission2.png",
    width=450,
    height=300,
    visible=False
)

mission_picture_3 = Picture(
    app,
    image="mission3.png",
    width=450,
    height=300,
    visible=False
)


tellolock = Lock()

tellocontrolthread = Thread(
    target=lambda: tellocontrolloop(
        tello,
        controller,
        tellolock
    ),
    daemon=True
)


telloupdatethread = Thread(
    target=lambda: telloupdateloop(
        tello,
        battery_text,
        mission_pad_text
    ),
    daemon=True
)

tellostatusthread = Thread(
    target=lambda: switch_status(
        tello,
        controller,
        tellolock,
        autonomous_text,
        mission_text,
        mission_picture_1,
        mission_picture_2,
        mission_picture_3
    ),
    daemon=True
)

tello.connect()
tello.set_mission_pad_detection_direction(0)

try:
    tellocontrolthread.start()
    telloupdatethread.start()
    tellostatusthread.start()
    app.display()
finally:
    tello.end()
