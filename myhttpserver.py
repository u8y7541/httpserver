import socket
from threading import Thread
class HttpServer:
    def __init__(self, file):
        self.servesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servesock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.file = file
        self.output = open('output.txt', 'a')
    def parse_request(self, c):
        global conn
        command = [i.decode() for i in c.split()]
        if command[1] == '/':
            command[1] = '/index.html'
        # try:
        global response
        response = bytes(self.construct_header(command[1]), 'ASCII')
        # except:
        #     print("Browser Refreshed/X'd out/Stopped loading")
        #     return
        if command[0] == 'GET':
            response += b'\n\n' + open(self.file + command[1], 'rb').read()
        else:
            var = list(c.decode().split('\n')[-1])
            var[var.index('=')] = ''
            var = [''.join(var[:var.index('')]), ''.join(var[var.index(''):])]
            c = c.decode()
            global data
            data = {}
            for i in ['Connection', 'Content-Length', 'Content-Type', 'User-Agent', 'Accept', 'Accept-Encoding', 'Accept-Language', 'Host']:
                for j in c.split('\n'):
                    if i in j:
                        value = c.split('\n')[c.split('\n').index(j)]
                        data[value[:value.index(':')]] = value[value.index(':') + 2:][:-1]
            data[var[0]] = var[1]
            dofile(command[1])
        try:
            print('Response:\n' + response.decode())
        except:
            print('Response is image.')
            print(response)
        conn.send(response)
        conn.close()
    def close(self):
        self.servesock.close()
        self.output.close()
    def listen(self):
        self.servesock.bind((socket.gethostname(), 80))
        self.servesock.listen(10)
        global conn
        while True:
            try:
                conn, addr = self.servesock.accept()
            except:
                print('Server closed')
            a = Thread(target = self.client)
            a.start()
            a.join()   
    def client(self):
        global conn
        connection = conn
        while True:
            try:
                a = connection.recv(2048)
            except:
                return
            print('Packet:\n' + a.decode())
            self.output.write(a.decode())
            self.parse_request(a)
    def construct_header(self, file):
        statline = ''
        try:
            open(self.file + file)
            statline = 'HTTP/1.1 200 OK'
        except:
            statline = 'HTTP/1.1 404 File Not Found'
        if any([i in file for i in ['.jpeg', '.png', '.ico', '.gif']]):
            return statline + '\r\nContent-Type: image/' + file.split('.')[1] + '\r\nContent-Length: ' + str(len(open(self.file + file, 'rb').read())) + '\r\n'
        return statline  + '\r\nContent-Type: text/html\r\nConnection: close\r\n'
def dofile(b):
    global data
    global response
    global a
    exec('global response\n' + open(a.file + b).read())
global a
a = HttpServer('C:/Python34/Ana\'s Website')
a.listen()
