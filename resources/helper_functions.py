from djitellopy import Tello
from resources.ControllerInput import XboxController
from guizero import Text
import time
from threading import Lock
from resources.constants import *
from threading import Thread, Lock

is_auton = False
side = "textron"
m_type = 1

def set_side(current: str) -> None:
    global side

    side = current

def triangulate_small(t: Tello) -> tuple:
    x_dist = t.get_mission_pad_distance_x()
    y_dist = t.get_mission_pad_distance_y()
    z_dist = t.get_mission_pad_distance_z()

    id = t.get_mission_pad_id()
    t.go_xyz_speed_mid(x=0, y=0, z=z_dist, speed=30, mid=id)


def triangulate_tall(t: Tello) -> tuple:
    x_dist = t.get_mission_pad_distance_x()
    y_dist = t.get_mission_pad_distance_y()
    z_dist = t.get_mission_pad_distance_z()

    id = t.get_mission_pad_id()
    t.go_xyz_speed_mid(x=0, y=0, z=z_dist, speed=30, mid=id)


def loop_forward(tello: Tello, dist: int, mp: int) -> None:
    while(tello.get_mission_pad_id() != mp):
        if not is_auton:
            break
        tello.move_forward(dist)


def map(x: float or int,
        in_min: float or int,
        in_max: float or int,
        out_min: float or int,
        out_max: float or int) -> float or int:
    """Maps input ranges to output ranges"""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def textron(tello: Tello, mission_type: int, lock: Lock) -> None:
    global is_auton
    #print("before lock")

    with lock:
        #print("after lock")
        if not tello.is_flying:
            tello.takeoff()

        tello.move_up(TEXTRON_SMALL_Y)
        
        #orient to direction of first building
        if(mission_type==1):
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

        tello.move_up(TEXTRON_MIDDLE_Y-TEXTRON_SMALL_Y) #Above first pad
        if not is_auton:
            return


        if(mission_type==1):
            tello.rotate_clockwise(45)
            loop_forward(tello, 40, 4)
            if not is_auton:
                return
            tello.rotate_counter_clockwise(45) #Above second pad
            if not is_auton:
                return
            
        else:
            tello.move_forward(40,4)
            if not is_auton:
                return

        triangulate_small(tello)
        if not is_auton:
            return
        triangulate_small(tello)
        if not is_auton:
            return
        #triangulated to MP4

        

        if(mission_type==1 or mission_type==3):
            tello.move_up(TEXTRON_TALL_Y) #move to height of tall buildings

            loop_forward(tello, 40, 6)
            if not is_auton:
                return
            triangulate_tall(tello)
            if not is_auton:
                return
            triangulate_tall(tello)
            if not is_auton:
                return
            #above MP6

            tello.rotate_counter_clockwise(90) #facing MP5

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
            loop_forward(tello, 40,3)
            triangulate_small(tello)
            if not is_auton:
                return
            tello.rotate_clockwise(90)
            triangulate_small(tello)
            if not is_auton:
                return
            #above MP3, facing MP5

            tello.move_up(TEXTRON_TALL_Y) #move to height of tall buildings
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


def residential(tello:Tello, mission_type:int, lock: Lock) -> None:
    global is_auton


    with lock:

        if not tello.is_flying:
            tello.takeoff()
        #residential
        tello.move_up(RESIDENTIAL_SMALL_Y)
        if not is_auton:
                return
        #orient to direction of first building
        if(mission_type==1):
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

        tello.move_up(RESIDENTIAL_MIDDLE_Y) #Above first pad
        


        if(mission_type==1):
            tello.rotate_clockwise(45)
            loop_forward(tello, 40, 4)
            tello.rotate_counter_clockwise(45) #Above second pad
            if not is_auton:
                return
            
        else:
            tello.move_forward(40,4)

        triangulate_small(tello)
        if not is_auton:
                return
        triangulate_small(tello)
        if not is_auton:
                return
        #triangulated to MP4

        

        if(mission_type==1 or mission_type==3):
            tello.move_up(RESIDENTIAL_TALL_Y) #move to height of tall buildings
            if not is_auton:
                return
            loop_forward(tello, 40, 6)
            triangulate_tall(tello)
            if not is_auton:
                return
            triangulate_tall(tello)
            if not is_auton:
                return
            #above MP6

            tello.rotate_counter_clockwise(90) #facing MP5
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
            loop_forward(tello, 40,3)
            triangulate_small(tello)
            if not is_auton:
                return
            tello.rotate_clockwise(90)
            if not is_auton:
                return
            triangulate_small(tello)
            if not is_auton:
                return
            #above MP3, facing MP5

            tello.move_up(RESIDENTIAL_TALL_Y) #move to height of tall buildings
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


def switch_status(tello: Tello, controller: XboxController, lock: Lock, auton_text: Text, mission_text: Text):
    """X to turn on, B to turn off"""

    global is_auton
    global m_type


    while True:
        try: 
            #print(f"{controller.X}")
            auton_text.value = f"Autonomous Mode: {is_auton}"
            mission_text.value =f"mission: {m_type}"

            left_pad = controller.LeftDPad
            up_pad = controller.UpDPad
            right_pad = controller.RightDPad

            if left_pad == 1 and left_pad != last_button_LeftDPad and not is_auton:
                m_type = 1
            if up_pad == 1 and up_pad != last_button_UpDPad and not is_auton:
                m_type = 2
            if right_pad == 1 and right_pad != last_button_RightDPad and not is_auton:
                m_type = 3



            if controller.X == 1 and controller.X != last_button_X and not is_auton:
                #print("2")
                is_auton = True
                if side=="textron":
                    Thread(target=lambda: textron(tello, mission_type=m_type, lock=lock), daemon=True).start() 
                elif side=="residential":
                    Thread(target=lambda: residential(tello, mission_type=m_type, lock=lock), daemon=True).start() 
            
            if controller.B == 1 and controller.B != last_button_B and  is_auton:
                is_auton = False

            last_button_LeftDPad = controller.LeftDPad
            last_button_UpDPad = controller.UpDPad
            last_button_RightDPad = controller.RightDPad
            last_button_B = controller.B
            last_button_X = controller.X
        except:
            pass


def tellocontrolloop(tello: Tello, controller: XboxController, lock: Lock):

    last_button_Y = 0
    while True:
        with lock:
            try: 
                #Check for Inputs
                if (controller.Y == 1) and not tello.is_flying and controller.Y != last_button_Y:
                    tello.takeoff()
                    
                elif controller.A == 1 and controller.A != last_button_A:
                    tello.land()
                last_button_Y = controller.Y
                last_button_A = controller.A

                #tJoystick Data
                left_stick_y = controller.LeftJoystickY 
                left_stick_x = controller.LeftJoystickX
                right_stick_y = controller.RightJoystickY 
                right_stick_x = controller.RightJoystickX 

                #Map from Joystick values to Input Values
                up_down = int(map(left_stick_y, -1, 1, -100, 100))
                yaw = int(map(left_stick_x, -1, 1, -100, 100))
                forward_backward = int(map(right_stick_y, -1, 1, -100, 100))
                left_right = int(map(right_stick_x, -1, 1, -100, 100))

                #Send Command to Tello
                tello.send_rc_control(left_right, forward_backward, up_down, yaw)
                
            except:
                pass

        pass


def telloupdateloop(tello: Tello, battery_text: Text, mission_pad_text: Text):


    while True:


        try: 

            #GUI updating
            mp = tello.get_mission_pad_id()
            battery = tello.get_battery()
            battery_text.value = f"Battery: {battery}%"
            mission_pad_text.value = f"MP: {mp}"
            time.sleep(1/10)
        
        except:
            pass

        pass