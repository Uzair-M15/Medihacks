import template
from http.server import SimpleHTTPRequestHandler
import socketserver
import atexit
import socket
from contextlib import closing
import definitions
import app.src.python.jdata as jdata

PORT = 808  #BOB

def find_port():
    for i in range(65535):
        with closing(socket.socket()) as sock :
            if sock.bind(('127.0.0.1' , i)) == 0:
                return i
            else : 
                pass
    
    return None

class CuraHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        split_path = self.path.split("/")
        if split_path[0] == "":
            split_path.pop(0)
        
        if self.path == '/':
            self.send_response(200 , 'OK')
            self.send_header('Content-type' , 'html')
            self.end_headers()
            self.wfile.write(template.load('./html/index.html'))
        elif self.path =='/home':
            self.send_response(200 , 'OK')
            self.send_header('Content-type' , 'html')
            self.end_headers()
            self.wfile.write(template.load('./html/home.html'))
        elif split_path[0] == 'send' :
            try :
                if split_path[1] == 'user':
                    self.send_response(200, 'OK')
                    self.send_header('Content-type' , 'html')
                    self.end_headers()
                    definitions.active_chat = f'{split_path[2]}'
                    self.wfile.write(template.load('./html/chat.html'))
            except IndexError :
                self.send_response(200, 'OK')
                self.send_header('Content-type' , 'html')
                self.end_headers()
                self.wfile.write(template.load('./html/send.html'))
        elif self.path == '/info':
            self.send_response(200 , 'OK')
            self.send_header('Content-type' , 'html')
            self.end_headers()
            self.wfile.write(template.load('./html/info.html'))
        else :
            dirs = self.path.split("/")
            if dirs[1] == 'image' :
                try :
                    f = open("./html/image/{}".format(dirs[2]) , 'rb')
                    image = bytes(f.read())
                    f.close()
                    self.send_response(200 , 'OK')
                    self.send_header('Content-type' , 'image/png')
                    self.end_headers()
                    self.wfile.write(image)
                except FileNotFoundError:
                    self.send_response(404 , 'Not Found')
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length"))
        request = self.rfile.read(length).decode()

        request = request.replace("+" , " ")

        if request.split("=")[0] == "message":
            data = request.split("=")[1]

        split_path = self.path.split("/")

        if split_path[1] == 'send' :
            try :
                if split_path[2] == 'user':
                    definitions.handler.Send(definitions.handler.ip_table.get_ip(definitions.active_chat) , jdata.Text_Message(data))
                    self.send_response(200, 'OK')
                    self.send_header('Content-type' , 'html')
                    self.end_headers()
                    self.wfile.write(template.load('./html/chat.html'))
            except IndexError :
                self.send_response(200, 'OK')
                self.send_header('Content-type' , 'html')
                self.end_headers()
                self.wfile.write(template.load('./html/send.html'))


def run():
    server = socketserver.TCPServer(('127.0.0.1' , PORT) , CuraHandler)
    print("Open in browser: http://127.0.0.1:{}/home".format(PORT.__str__()))
    server.serve_forever()
    atexit(server.shutdown())

if __name__ == "__main__":
    run()