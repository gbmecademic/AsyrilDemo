import socket


class EyePlusClient:

    def __init__(self):
        self.__connection = None
        self.termination = "\n"

    def connect(self, ipaddress, port):
        self.ipaddress = ipaddress
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.connect((self.ipaddress, port))

    def disconnect(self):
        self.__connection.close()
        self.__connection = None

    def stop_production(self):
        command = "stop production"
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def start_production(self, recipe):
        command = "start production " + str(recipe)
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def get_part(self):
        command = "get_part"
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def force_take_image(self):
        command = "force_take_image"
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def prepare_part(self):
        command = "prepare_part"
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def can_take_image(self, value):
        command = "can_take_image " + str(value).lower()
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def set_parameter(self, parameter):
        command = "set_parameter " + str(parameter)
        self.__send_raw__(command)
        response = self.__receive_raw__()
        return response

    def __send_raw__(self, command):
        self.__connection.send(
            bytes(f'{command}{self.termination}', encoding="ascii"))

    def __receive_raw__(self):
        response = self.__connection.recv(4096).decode("ascii")
        return response

    @staticmethod
    def extract_status(response):
        status = int(response[:3])
        return status

    @staticmethod
    def extract_position(response: str):
        split_response = response.split(' ')
        x = float(split_response[1][2:])
        y = float(split_response[2][2:])
        rz = float(split_response[3][3:])
        return [x, y, rz]
