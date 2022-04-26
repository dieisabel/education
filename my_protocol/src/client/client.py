import socket


class Client:
    def __init__(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, ipv4, port):
        pass


def client():
    s = Socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDR)


    while True:
        data = input('Enter data: ')
        s.send(data.encode('utf-8'))

        response = s.recv(1024)
        print(response.decode('utf-8'))


if __name__ == '__main__':
    client()
