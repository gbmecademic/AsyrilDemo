from eyeplus import EyePlusClient

camera = EyePlusClient()
camera.connect('192.168.1.50', 7171)


camera.start_production(25892)

while True:
    usr_input = input('Enter quit to leave otherwise press Enter: ')

    if usr_input == 'quit':
        camera.stop_production()
        break

    response = camera.get_part()
    if camera.extract_status(response) != 200:
        print('Error with get_part')
        camera.stop_production()
        break

    print(camera.extract_position(response))
