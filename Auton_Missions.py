from djitellopy import Tello


FIRESTATION_TO_FIRSTBUILDING_LATERAL = 35

#Test values no y heights

TEXTRON_TALL_Y = 20
TEXTRON_MIDDLE_Y = 40
TEXTRON_SMALL_Y = 20

#TEXTRON TOWERS y Values CM

#TEXTRON_TALL_Y = 200 
#TEXTRON_MIDDLE_Y = 80
#TEXTRON_SMALL_Y = 20


#Residential District y Values CM

RESIDENTIAL_TALL_Y = 165
RESIDENTIAL_MIDDLE_Y = 127
RESIDENTIAL_SMALL_Y = 20




tello = Tello()

tello.connect()
tello.set_mission_pad_detection_direction(0)
tello.set_speed(40)


def side(side: str ="textron") -> bool:
    """either pass 'Ttextron' or "residential' """
    return True if side=="textron".lower() else False
def mission(m: int = 1) -> int:
    return int


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
    t.go_xyz_speed_mid(z=z_dist, speed=30, mid=id)

def loop_forward(dist: int, mp: int) -> None:
    while(tello.get_mission_pad_id() != mp):
        tello.move_forward(dist)
    

#pass residential if the side is residential
burn = str(input("which side textron, or residential: "))
is_textron = side(burn)

#1 -3
miss = int(input("mission type, 1, 2, or 3: "))
mission_type = 1

# Mission
tello.takeoff()

if(is_textron):
    #Textron Towers

    tello.move_up(TEXTRON_SMALL_Y)
    
    #orient to direction of first building
    if(mission_type==1):
        tello.move_left(FIRESTATION_TO_FIRSTBUILDING_LATERAL)
    else:
        tello.move_right(FIRESTATION_TO_FIRSTBUILDING_LATERAL)


    loop_forward(40, 1) if mission_type == 1 else loop_forward(40, 2)
    
    
    triangulate_small(tello)
    triangulate_small(tello)

    tello.move_up(TEXTRON_MIDDLE_Y-TEXTRON_SMALL_Y) #Above first pad
    


    if(mission_type==1):
        tello.rotate_clockwise(45)
        loop_forward(40, 4)
        tello.rotate_counter_clockwise(45) #Above second pad
        
    else:
        tello.move_forward(40,4)

    triangulate_small(tello)
    triangulate_small(tello)
    #triangulated to MP4

    

    if(mission_type==1 or mission_type==3):
        tello.move_up(TEXTRON_TALL_Y) #move to height of tall buildings

        loop_forward(40, 6)
        triangulate_tall(tello)
        triangulate_tall(tello)
        #above MP6

        tello.rotate_counter_clockwise(90) #facing MP5

        loop_forward(40, 5)
        triangulate_small(tello)
        triangulate_small(tello)
        tello.land()


    else:
        tello.rotate_counter_clockwise(90)
        loop_forward(40,3)
        triangulate_small(tello)
        tello.rotate_clockwise(90)
        triangulate_small(tello)
        #above MP3, facing MP5

        tello.move_up(TEXTRON_TALL_Y) #move to height of tall buildings

        loop_forward(40, 5)
        triangulate_small(tello)
        triangulate_small(tello)
        tello.land()
    



else:
    #residential
    tello.move_up(RESIDENTIAL_SMALL_Y)
    
    #orient to direction of first building
    if(mission_type==1):
        tello.move_left(FIRESTATION_TO_FIRSTBUILDING_LATERAL)
    else:
        tello.move_right(FIRESTATION_TO_FIRSTBUILDING_LATERAL)


    loop_forward(40, 1) if mission_type == 1 else loop_forward(40, 2)
    
    
    triangulate_small(tello)
    triangulate_small(tello)

    tello.move_up(RESIDENTIAL_MIDDLE_Y) #Above first pad
    


    if(mission_type==1):
        tello.rotate_clockwise(45)
        loop_forward(40, 4)
        tello.rotate_counter_clockwise(45) #Above second pad
        
    else:
        tello.move_forward(40,4)

    triangulate_small(tello)
    triangulate_small(tello)
    #triangulated to MP4

    

    if(mission_type==1 or mission_type==3):
        tello.move_up(RESIDENTIAL_TALL_Y) #move to height of tall buildings

        loop_forward(40, 6)
        triangulate_tall(tello)
        triangulate_tall(tello)
        #above MP6

        tello.rotate_counter_clockwise(90) #facing MP5

        loop_forward(40, 5)
        triangulate_small(tello)
        triangulate_small(tello)
        tello.land()


    else:
        tello.rotate_counter_clockwise(90)
        loop_forward(40,3)
        triangulate_small(tello)
        tello.rotate_clockwise(90)
        triangulate_small(tello)
        #above MP3, facing MP5

        tello.move_up(RESIDENTIAL_TALL_Y) #move to height of tall buildings

        loop_forward(40, 5)
        triangulate_small(tello)
        triangulate_small(tello)
        tello.land()

tello.end()

