import socketio

class SocketClient():
    def __init__(self):
        self.sio = socketio.Client()
        self.ip = 'http://127.0.0.1:5036'
        self.sio.connect(self.ip)               
        
        
    def send(self, message):
        self.sio.emit('message', message)

if __name__ == '__main__':
    sc = SocketClient()
    sc.send('Hello World')