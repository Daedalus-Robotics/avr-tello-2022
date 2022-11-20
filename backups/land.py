from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()
time.sleep(200)
tello.land()