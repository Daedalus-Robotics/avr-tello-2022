from resources.constants import * 
from resources.helper_functions import *
from guizero import App, Text
from djitellopy import Tello
from threading import Thread, Lock
from resources.ControllerInput import XboxController



app = App(title="tello-control")
controller = XboxController()
tello = Tello()

#Button Variables
mp = -1
battery = -1
mission_pad_text = Text(app, text=f"MP: {mp}")
battery_text = Text(app, text=f"Battery: {battery}%")
tellolock = Lock()

tellocontrolthread = Thread(target=lambda: tellocontrolloop(tello, controller, tellolock), daemon=True)
telloupdatethread = Thread(target=lambda: telloupdateloop(tello, battery_text, mission_pad_text), daemon=True)
tellostatusthread = Thread(target=lambda: switch_status(tello, controller, tellolock), daemon=True)

tello.connect()
tello.set_mission_pad_detection_direction(0)



#buttons_text = Text(app, text=f"Buttons: {controller.read()}")

try: 
    tellocontrolthread.start()
    telloupdatethread.start()
    tellostatusthread.start()
    app.display()
finally:
    tello.end()


