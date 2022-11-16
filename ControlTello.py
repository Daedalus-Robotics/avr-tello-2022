from guizero import App, Text
from djitellopy import Tello
from threading import Thread
from ControllerInput import XboxController
import numpy as np
import cv2
from PIL import Image, ImageTk
import tkinter

app = App(title="tello-control")
controller = XboxController()
tello = Tello()
tello.connect()
#tello.takeoff()
#tello.streamoff()
tello.set_mission_pad_detection_direction(0)
"""tello.streamon()
print(tello.get_udp_video_address())
drone_video_capture = tello.get_video_capture()"""




def map(x: float or int,
        in_min: float or int,
        in_max: float or int,
        out_min: float or int,
        out_max: float or int) -> float or int:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def telloloop():
    last_button_Y = 0
    while True:

        if (controller.Y == 1) and not tello.is_flying and controller.Y != last_button_Y:
            tello.takeoff()
            
        elif controller.A == 1:
            tello.land()
        last_button_Y = controller.Y
        #tello control code
        left_stick_y = controller.LeftJoystickY 
        left_stick_x = controller.LeftJoystickX
        right_stick_y = controller.RightJoystickY 
        right_stick_x = controller.RightJoystickX 

        up_down = int(map(left_stick_y, -1, 1, -100, 100))
        yaw = int(map(left_stick_x, -1, 1, -100, 100))
        forward_backward = int(map(right_stick_y, -1, 1, -100, 100))
        left_right = int(map(right_stick_x, -1, 1, -100, 100))

        tello.send_rc_control(left_right, forward_backward, up_down, yaw)

        #GUI updating
        mp = tello.get_mission_pad_id()
        battery = tello.get_battery()
        battery_text.value = f"Battery: {battery}%"
        mission_pad_text.value = f"MP: {mp}"
        #buttons_text.value = f"Buttons: {controller.read()}"

        """#got_frame = True
        got_frame, frame = drone_video_capture.read()
        
        if got_frame:
            frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
            bottom_camera.imgtk = frame
            bottom_camera.configure(image=frame)""" 
        

        pass

tellothread = Thread(target=telloloop, daemon=True)



mp = -1
battery = -1

mission_pad_text = Text(app, text=f"MP: {mp}")
battery_text = Text(app, text=f"Battery: {battery}%")
#buttons_text = Text(app, text=f"Buttons: {controller.read()}")

"""bottom_camera = tkinter.Label(width=200, height=200)
bottom_camera.pack
app.add_tk_widget(bottom_camera)"""


tellothread.start()
"""while True:
    print(drone_video_capture)
    got_frame, frame = drone_video_capture.read()
    if got_frame:
        cv2.imshow("A", frame)
        cv2.waitKey(1)"""
app.display()
#tello.streamoff()