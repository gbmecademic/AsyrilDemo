from eyeplus import EyePlusClient
from mecademicpy.robot import Robot
from positions import *

camera = EyePlusClient()
camera.connect('192.168.1.50', 7171)

robot = Robot()
robot.Connect('192.168.1.100')
robot.SetTrf(*TRF_PICK)
robot.SetJointVel(10)
robot.SetCartLinVel(25)
robot.SetGripperForce(10)
robot.SetGripperVel(20)
robot.SetGripperRange(0, 14)

robot.MoveJoints(*SAFE_POS_FRONT)
robot.WaitIdle()

camera.start_production(25892)

while True:
    usr_input = input('Enter quit to leave otherwise press Enter: ')
    robot.GripperOpen()
    robot.Delay(3)

    if usr_input == 'quit':
        camera.stop_production()
        break

    response = camera.get_part()
    if camera.extract_status(response) != 200:
        print('Error with get_part')
        camera.stop_production()
        break

    poses = camera.extract_position(response)

    robot.MovePose(*SAFE_POS_FEED)
    robot.MovePose(poses[0], poses[1], Z_POS+30, 0, 0, poses[2])
    robot.Delay(2)
    robot.MoveLin(poses[0], poses[1], Z_POS, 0, 0, poses[2])
    robot.GripperClose()
    robot.Delay(0.5)
    robot.MoveLin(poses[0], poses[1], Z_POS+40, 0, 0, poses[2])
    robot.MovePose(*SAFE_POS_FEED)
    robot.MoveJoints(*SAFE_POS_FRONT)


robot.Disconnect()
