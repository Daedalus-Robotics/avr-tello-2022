from djitellopy import Tello
from lib.ControllerInput import XboxController
from guizero import Text, Picture
from lib.constants import *
from threading import Thread, Lock
import time

# Global Variables
is_auton = False
side = "textron"
m_type = -1


def set_side(current: str) -> None:
    global side

    side = current


def triangulate_small(t: Tello) -> None:
    z_dist = t.get_mission_pad_distance_z()

    mid = t.get_mission_pad_id()
    t.go_xyz_speed_mid(x=0, y=0, z=z_dist, speed=30, mid=mid)


def triangulate_tall(t: Tello) -> None:
    z_dist = t.get_mission_pad_distance_z()

    mid = t.get_mission_pad_id()
    t.go_xyz_speed_mid(x=0, y=0, z=z_dist, speed=30, mid=mid)


def loop_forward(tello: Tello, dist: int, mp: int) -> None:
    while tello.get_mission_pad_id() != mp:
        if not is_auton:
            break
        tello.move_forward(dist)


def loop_down_to_mission_pad(tello: Tello, _mp: int, dist: int = 20) -> None:
    while tello.get_mission_pad_distance_y() > 30:
        if not is_auton:
            break
        tello.move_down(dist)


def map_joysticks(x: float or int,
                  in_min: float or int,
                  in_max: float or int,
                  out_min: float or int,
                  out_max: float or int) -> float or int:
    """Maps input ranges to output ranges"""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def textron(tello: Tello, mission_type: int, lock: Lock) -> None:
    global is_auton

    with lock:

        time.sleep(.1)

        if not tello.is_flying:
            tello.takeoff()

        tello.move_up(TEXTRON_SMALL_Y)

        # Orient to direction of first building
        if mission_type == 1:
            tello.move_left(FIRESTATION_TO_FIRSTBUILDING_LATERAL)
        else:
            tello.move_right(FIRESTATION_TO_FIRSTBUILDING_LATERAL)

        if not is_auton:
            return

        loop_forward(tello, 40, 1) if mission_type == 1 else loop_forward(tello, 40, 2)

        triangulate_small(tello)
        if not is_auton:
            return
        triangulate_small(tello)
        if not is_auton:
            return

        tello.move_up(TEXTRON_MIDDLE_Y - TEXTRON_SMALL_Y)  # Above first pad

        if not is_auton:
            return

        if mission_type == 1:
            tello.rotate_clockwise(58)
            loop_forward(tello, 40, 4)
            if not is_auton:
                return
            tello.rotate_counter_clockwise(58)  # Above second pad
            if not is_auton:
                return
        else:
            tello.move_left(20)
            loop_forward(tello, 40, 4)

            if not is_auton:
                return

        triangulate_small(tello)

        if not is_auton:
            return

        triangulate_small(tello)

        if not is_auton:
            return

        # Triangulated to MP4

        if mission_type == 1 or mission_type == 3:
            tello.move_up(TEXTRON_TALL_Y)  # Move to height of tall buildings

            loop_forward(tello, 40, 6)

            if not is_auton:
                return

            triangulate_tall(tello)

            if not is_auton:
                return

            triangulate_tall(tello)

            if not is_auton:
                return

            # Above MP6

            tello.rotate_counter_clockwise(90)  # Facing MP5

            loop_forward(tello, 40, 5)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            tello.land()
        else:
            tello.rotate_counter_clockwise(90)
            loop_forward(tello, 40, 3)
            triangulate_small(tello)

            if not is_auton:
                return

            tello.rotate_clockwise(90)
            triangulate_small(tello)

            if not is_auton:
                return

            # Above MP3, facing MP5

            tello.move_up(TEXTRON_TALL_Y)  # Move to height of tall buildings

            if not is_auton:
                return

            loop_forward(tello, 40, 5)
            triangulate_small(tello)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            tello.land()

        is_auton = False


def residential(tello: Tello, mission_type: int, lock: Lock) -> None:
    global is_auton

    with lock:

        time.sleep(.1)

        if not tello.is_flying:
            tello.takeoff()

        tello.move_up(RESIDENTIAL_SMALL_Y)

        if not is_auton:
            return

        # Orient to direction of first building
        if mission_type == 1:
            tello.move_left(FIRESTATION_TO_FIRSTBUILDING_LATERAL)
        else:
            tello.move_right(FIRESTATION_TO_FIRSTBUILDING_LATERAL)
        if not is_auton:
            return

        loop_forward(tello, 40, 1) if mission_type == 1 else loop_forward(tello, 40, 2)

        triangulate_small(tello)

        if not is_auton:
            return
        triangulate_small(tello)

        if not is_auton:
            return

        tello.move_up(RESIDENTIAL_MIDDLE_Y)  # Above first pad

        if mission_type == 1:
            tello.rotate_clockwise(55)
            loop_forward(tello, 40, 4)
            tello.rotate_counter_clockwise(55)  # Above second pad
            if not is_auton:
                return
        else:
            tello.move_left(20)
            loop_forward(tello, 40, 4)

        triangulate_small(tello)

        if not is_auton:
            return

        triangulate_small(tello)

        if not is_auton:
            return

        # Triangulated to MP4

        if mission_type == 1 or mission_type == 3:
            # Move to height of tall buildings
            tello.move_up(RESIDENTIAL_TALL_Y)

            if not is_auton:
                return

            loop_forward(tello, 40, 6)
            triangulate_tall(tello)

            if not is_auton:
                return

            triangulate_tall(tello)

            if not is_auton:
                return

            # Above MP6

            tello.rotate_counter_clockwise(90)  # Facing MP5

            if not is_auton:
                return

            loop_forward(tello, 40, 5)
            triangulate_small(tello)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            tello.land()
        else:
            tello.rotate_counter_clockwise(90)

            if not is_auton:
                return

            loop_forward(tello, 40, 3)
            triangulate_small(tello)

            if not is_auton:
                return

            tello.rotate_clockwise(90)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            # Above MP3, facing MP5

            # Move to height of tall buildings
            tello.move_up(RESIDENTIAL_TALL_Y)

            if not is_auton:
                return

            loop_forward(tello, 40, 5)
            triangulate_small(tello)

            if not is_auton:
                return

            triangulate_small(tello)

            if not is_auton:
                return

            tello.land()

        is_auton = False


def land_textron(tello: Tello, lock: Lock) -> None:
    with lock:
        # Either tall closed roof or tall open roof
        start_pad = tello.get_mission_pad_id()

        # Make sure it is over the pad
        triangulate_small(tello)
        loop_down_to_mission_pad(tello, tello.get_mission_pad_id())
        triangulate_small(tello)

        tello.move_forward(40)
        tello.move_down(TEXTRON_TALL_Y)

        loop_forward(tello, dist=20, mp=(3 if start_pad == 5 else 4))

        triangulate_small(tello)

        loop_forward(tello, dist=20, mp=(1 if start_pad == 5 else 2))

        triangulate_small(tello)

        loop_forward(tello, dist=20, mp=(7 if start_pad == 5 else 8))

        triangulate_small(tello)

        if tello.get_height() > 20:
            tello.move_down(20)

        triangulate_small(tello)

        tello.land()


def land_residential(tello: Tello, lock: Lock) -> None:
    with lock:
        # Either tall closed roof or tall open roof
        start_pad = tello.get_mission_pad_id()

        # Make sure it is over the pad
        triangulate_small(tello)
        loop_down_to_mission_pad(tello, tello.get_mission_pad_id())
        triangulate_small(tello)

        tello.move_forward(40)
        tello.move_down(RESIDENTIAL_TALL_Y)

        loop_forward(tello, dist=20, mp=(3 if start_pad == 5 else 4))

        triangulate_small(tello)

        loop_forward(tello, dist=20, mp=(1 if start_pad == 5 else 2))

        triangulate_small(tello)

        loop_forward(tello, dist=20, mp=(7 if start_pad == 5 else 8))

        triangulate_small(tello)

        if tello.get_height() > 20:
            tello.move_down(20)

        triangulate_small(tello)

        tello.land()


def switch_status(tello: Tello,
                  controller: XboxController,
                  lock: Lock,
                  auton_text: Text,
                  mission_text: Text,
                  mission_picture_1: Picture,
                  mission_picture_2: Picture,
                  mission_picture_3: Picture,
                  basepads_picture: Picture) -> None:
    """X to turn on, B to turn off"""

    global is_auton
    global m_type

    last_button_left_d_pad = 0
    last_button_up_d_pad = 0
    last_button_right_d_pad = 0
    last_button_down_d_pad = 0
    last_button_b = 0
    last_button_x = 0

    while True:

        try:

            if controller.B == 1 and controller.B != last_button_b and is_auton:
                is_auton = False

            # update autonomous text box and mission number
            auton_text.value = f"Autonomous Mode: {is_auton}"
            mission_text.value = f"mission: {m_type}"

            # takes current input from controller
            left_pad = controller.LeftDPad
            up_pad = controller.UpDPad
            right_pad = controller.RightDPad
            down_pad = controller.DownDPad

            # changes mission type based on buttons pressed

            if left_pad == 1 and left_pad != last_button_left_d_pad and not is_auton:
                m_type = 1
                mission_picture_1.visible = True
                mission_picture_2.visible = False
                mission_picture_3.visible = False
                basepads_picture.visible = False
            if up_pad == 1 and up_pad != last_button_up_d_pad and not is_auton:
                m_type = 2
                mission_picture_1.visible = False
                mission_picture_2.visible = True
                mission_picture_3.visible = False
                basepads_picture.visible = False
            if right_pad == 1 and right_pad != last_button_right_d_pad and not is_auton:
                m_type = 3
                mission_picture_1.visible = False
                mission_picture_2.visible = False
                mission_picture_3.visible = True
                basepads_picture.visible = False
            if down_pad == 1 and down_pad != last_button_down_d_pad and not is_auton:
                m_type = -1
                mission_picture_1.visible = False
                mission_picture_2.visible = False
                mission_picture_3.visible = False
                basepads_picture.visible = True

            # As long as a mission (1-3) is selected it activates autonomy
            if m_type == -1:
                continue
            elif controller.X == 1 and controller.X != last_button_x and not is_auton:
                is_auton = True
                if side == "textron":

                    Thread(
                        target=lambda: textron(
                            tello,
                            mission_type=m_type,
                            lock=lock
                        ),
                        daemon=True
                    ).start()

                elif side == "residential":

                    Thread(
                        target=lambda: residential(
                            tello,
                            mission_type=m_type,
                            lock=lock
                        ),
                        daemon=True
                    ).start()

            # Sets last buttons for comparison
            last_button_left_d_pad = controller.LeftDPad
            last_button_up_d_pad = controller.UpDPad
            last_button_right_d_pad = controller.RightDPad
            last_button_down_d_pad = controller.DownDPad
            last_button_b = controller.B
            last_button_x = controller.X

        except Exception as e:
            print(f"{e}")
            pass


def tello_control_loop(tello: Tello, controller: XboxController, lock: Lock):
    while True:
        with lock:

            time.sleep(.1)

            try:

                # Check for inputs
                if controller.Y == 1 and not tello.is_flying and controller.Y != last_button_Y:
                    print("y, pressed")
                    tello.takeoff()

                elif controller.A == 1 and controller.A != last_button_A:
                    tello.land()

                # Sets last buttons for comparison
                last_button_Y = controller.Y
                last_button_A = controller.A

                # Joystick Data
                left_stick_y = controller.LeftJoystickY
                left_stick_x = controller.LeftJoystickX
                right_stick_y = controller.RightJoystickY
                right_stick_x = controller.RightJoystickX

                # Map from Joystick values to Input Values
                up_down = int(map_joysticks(left_stick_y, -1, 1, -100, 100))
                yaw = int(map_joysticks(left_stick_x, -1, 1, -100, 100))
                forward_backward = int(map_joysticks(right_stick_y, -1, 1, -100, 100))
                left_right = int(map_joysticks(right_stick_x, -1, 1, -100, 100))

                # Send Command to Tello
                tello.send_rc_control(left_right, forward_backward,
                                      up_down, yaw)

            except Exception as e:
                print(f"{e}")
                pass

        pass


def tello_update_loop(tello: Tello, battery_text: Text, mission_pad_text: Text):
    while True:

        try:

            # GUI updating
            mp = tello.get_mission_pad_id()
            battery = tello.get_battery()
            battery_text.value = f"Battery: {battery}%"
            mission_pad_text.value = f"MP: {mp}"
            time.sleep(1 / 10)

        except Exception as e:
            print(f"{e}")
            pass

        pass