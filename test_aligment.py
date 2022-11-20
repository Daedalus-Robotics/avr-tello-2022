from djitellopy import Tello



tello = Tello()

tello.connect()

tello.takeoff()


tello.go_xyz_speed_yaw_mid()