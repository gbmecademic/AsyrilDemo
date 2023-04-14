from mecademicpy.robot import Robot
from eyeplus import EyePlusClient
from positions import *


### Connect and initialize the robot ###
robot = Robot()
robot.Connect('192.168.1.100')
robot.ClearMotion()
robot.ResumeMotion()
robot.ActivateAndHome()
robot.WaitHomed()

# Move the robot to safe start position
robot.SetWrf(0, 0, 0, 0, 0, 0)
robot.SetTrf(*TRF_PICK)
robot.SetJointVel(HIGH_SPEED_JOINT)
robot.SetCartLinVel(LOW_SPEED_LIN)
robot.SetGripperForce(10)
robot.SetGripperVel(20)
robot.SetGripperRange(0, 13)
robot.MoveJoints(*SAFE_POS_FRONT)
robot.WaitIdle()

### Connect and start the camera and feeder ###
camera = EyePlusClient()
camera_IP = '192.168.1.50'
camera_PORT = 7171
camera.connect(camera_IP, camera_PORT)
camera.stop_production()
response_code = camera.extract_status(camera.start_production(25892))
if response_code != 200:
    raise Exception('Could not start production')

### Initialize the application ###
rack_full = False
vial_number = 0


### Main loop ###
while True:
    ### Check the state of the application ###
    if rack_full:
        rack_full = False
        vial_number = 0
        for pos in PLACE_POS:
            robot.SetTrf(*TRF_PLACE)
            robot.MovePose(*SAFE_POS_VIALS)
            robot.SetWrf(*pos, 0, 0, 0)
            robot.MovePose(0, -35, 55, *PLACE_ANGLE)
            robot.MoveLin(0, 0, 55, *PLACE_ANGLE)
            robot.MoveLin(0, 0, 0, *PLACE_ANGLE)
            robot.GripperClose()
            robot.Delay(0.5)
            robot.MoveLin(0, 0, 55, *PLACE_ANGLE)
            robot.SetWrf(0, 0, 0, 0, 0, 0)
            robot.MovePose(*SAFE_POS_VIALS)
            robot.MoveJoints(*SAFE_POS_FRONT)
            robot.SetTrf(*TRF_PICK)
            robot.MovePose(*SAFE_POS_FEED)
            robot.MovePose(*DROP_FEED)
            robot.GripperOpen()
            robot.Delay(0.2)
            robot.MoveJoints(*SAFE_POS_FRONT)
            cp = robot.SetCheckpoint(42)
            cp.wait()
            camera.force_take_image()

    robot.GripperOpen()
    robot.MoveJoints(*SAFE_POS_FRONT)
    robot.SetTrf(*TRF_PICK)
    robot.SetWrf(0, 0, 0, 0, 0, 0)
    robot.WaitIdle()

    ### Get the part position ###
    response = camera.get_part()
    if camera.extract_status(response) != 200:
        print(response)
        raise Exception('Problem with the Get Part')
    part_pos = camera.extract_position(response)

    ### Move the robot to pick the part ###
    robot.MovePose(*SAFE_POS_FEED)
    robot.MovePose(part_pos[0], part_pos[1], Z_POS+30, 0, 0, part_pos[2])
    robot.MoveLin(part_pos[0], part_pos[1], Z_POS, 0, 0, part_pos[2])
    robot.GripperClose()
    robot.Delay(0.5)
    robot.MoveLin(part_pos[0], part_pos[1], Z_POS+40, 0, 0, part_pos[2])
    robot.MovePose(*SAFE_POS_FEED)
    robot.MoveJoints(*SAFE_POS_FRONT)
    robot.SetTrf(*TRF_PLACE)

    ### Move the robot to the drop points and increment the vial_number ###
    robot.MovePose(*SAFE_POS_VIALS)
    robot.SetWrf(*PLACE_POS[vial_number], 0, 0, 0)
    robot.MovePose(0, 0, 40, *PLACE_ANGLE)
    robot.MoveLin(0, 0, 0, *PLACE_ANGLE)
    robot.GripperOpen()
    robot.Delay(0.5)
    robot.MoveLin(0, 0, 55, *PLACE_ANGLE)
    robot.MoveLin(0, -35, 55, *PLACE_ANGLE)
    robot.SetWrf(0, 0, 0, 0, 0, 0)
    robot.MovePose(*SAFE_POS_VIALS)
    robot.MoveJoints(*SAFE_POS_FRONT)
    cp = robot.SetCheckpoint(69)  # Nice
    cp.wait()

    vial_number += 1

    # Check if the vial number is greated than the limit
    if vial_number >= len(PLACE_POS):
        vial_number = 0
        rack_full = True

camera.stop_production()
robot.Disconnect()
