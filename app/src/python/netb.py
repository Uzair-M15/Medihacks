
import requests
import socket
from multiprocessing import Process
import json
import subprocess
import asyncio
import os







ip_table = None
PORT= 8008
BUFFER_SIZE = 4096
SERVICE_TOKEN = 'nbp_uhFD8nKYULoPNz6WZlKoY34LxRBv9B0nt3Fv'




class IPTable:

    def __init__(self):
        self.list = []
    
    def add_address(self, ip : str , hostname:str , id:str):
        if ip not in self.list:
            self.list.append((ip , hostname , id))
        else:
            print("Address already exists. Ignoring")

    def get_list(self):
        return self.list

    def hostnames(self):
        hosts = []
        for i in self.list:
            hosts.append(i[1])
        
        return hosts

    def IDs(self):
        ids = []
        for i in self.list:
            ids.append(i[2])
        
        return ids
    
    def IPs(self):
        ips = []

        for i in self.list:
            ips.append(i[0])
        
        return ips

    def __str__(self):
        table_string = ''
        for i in self.list:
            table_string = table_string + '\n' + i[0] + ':' + i[1]
        
        return table_string
    
    def get_ip(self , hostname):
        if hostname in self.IPs():
            return hostname
        for i in self.list:
            if hostname == i[1]:
                return i[0]
        return None
    
    def get_hostname(self , ip):
        if ip in self.hostnames():
            return ip
        for i in self.list:
            if ip == i[0]:
                return i[1]
        return None

    def get_id(self , ip) :
        if ip in self.IDs():
            return ip
        for i in self.list:
            if ip==i[1]:
                return i[2]




class ConnectionHandler:
    '''Asyncronously manages connection processes (Sending, Receiving)'''
    def __init__(self):
        #SERVER CODE
        #[( address , socket object ) , ...]
        self.connected_peers = []
        self.ip = self.whatismyip()
        self.ip_table = IPTable()

        #local server
        self.server_sock = socket.socket()
        self.server_sock.bind(( self.whatismyip ,PORT))
        self.max_connections = 50




        #CLIENT CODE
        self.client_sock = socket.socket()



        #storing communication
        self.stream = []

        handler_process = Process(target=self.ProcessRunner)
        handler_process.daemon = True
        handler_process.start()

    #region server_sock code
    def GetSock(self , address)->socket.socket|None:
        '''Returns the socket associated with an address.\n 
           If the address is not among the connected peers then None is returned\n
           Dont use method. Since Connections are made only when sending and \n     
           then closed after, this function is unreliable'''
        for i in self.connected_peers :
            if i[0] == address:
                return i[1]
        return None

    def ServerSend(self,address , message):
        try:
            msg = {
                "type":message.type,
                "format":message.format,
                "content":message.content,
                "to" : address,
                "from" : self.whatismyip()
            }
            msg = json.dumps(msg)
            self.stream.append(msg)
            self.GetSock(address).send(msg.encode())
        except :
            raise "Message might not be a valid jdata.Message object. Cancelling"
    
    def Receive(self , address):
        #add implementation for notifications
        print("Preparing to receive message from {}".format(address))
        sock = self.GetSock(address)
        if sock != None:
            message = sock.recv(BUFFER_SIZE)
            message = message.decode()
            self.stream.append(message)
            print(message)
        else:
            print("Socket for {} not found. Message was not received!".format(address))

        #handling input
        message = json.loads(message)
        if message["type"]=="message":
            host = ip_table.get_hostname(address)
            chat = open('../chats/{}.txt'.format())
            chat.write(message)
            chat.close()

    async def AcceptConnection(self):
        while True :
            self.server_sock.listen()
            conn,address = self.server_sock.accept()
            self.connected_peers.append(address[0] , conn)
            print("Connection Accepted for address :{}".format(address[0]))
            self.Receive(address=address)

    #endregion
    
    #region client_sock code

    def Connect(self , address):
        try:
            self.client_sock.connect((address, PORT))
            return 0
        except Exception as e:
            print("An error occured while connecting with message :",e)
            return 1
    
    def Disconnect(self):
        self.client_sock.close()
    
    def Send(self , address , message):
        try:
            if self.Connect(address)== 0:
                message = {
                    "type":message.type, 
                    "format" : message.format,
                    "to" : address , 
                    "from" : self.whatismyip(),
                    "content" : message.content
                }
                self.client_sock.send(message.to_str())
            else:
                print("Cant send message to address:{}".format(address))
        except:
            raise "Message might not be a valid jdata.Message object. Cancelling"

    #endregion

    def ProcessRunner(self):
        print('Child process started with id:{}'.format(os.getpid()))
        print("This process' Parent id :{}".format(os.getppid()))
        while True:
            self.getPeers()
            asyncio.run(self.AcceptConnection())

    #Update IP table
    def getPeers(self)->IPTable:
        headers = {
            'Accept' : 'application/json' ,
            'Authorization': 'Token {}'.format(SERVICE_TOKEN)
            }
        response = requests.request('get' ,'https://api.netbird.io/api/peers' , headers=headers)
        response=response.json()
        #Make IP Table
        table = IPTable()

        for i in response:
            table.add_address(i["ip"] , i["hostname"] , i["id"])
        
        if self.ip_table.list != table.list :
            self.ip_table = table
            print("[=] Update to IP Table :\n"+self.ip_table.__str__())

    def whatismyip(self)->str:
        '''Returns the the users netbird ip address'''
        process = subprocess.Popen("netbird status" , shell=True , stdout=subprocess.PIPE , stderr = subprocess.PIPE)
        process.wait()
        output = process.stdout.read().decode()

        output = output.split("\n")

        i = 0
        
        for line in output :
            if line.startswith("NetBird IP"):
                ip =line.partition(":")
                ip = ip[2]
                ip = ip.strip()
        
        ip = ip.partition("/")
        return ip[0]

    def whatismyid(self)->str:
        '''Returns the users netbird id. Requires refresh_table process to be running. Call RunService() to start the process'''
        try:
            my_ip = self.whatismyip()
            self.getPeers()
            for i in self.ip_table.list:
                if i[0] == my_ip:
                    return i[2]
        except :
            raise "Failed! Check if refresh_table process is running. If not call RunService()"

    def whatismyhostname(self)->str:
        '''Returns the users netbird hostname'''
        try:        
                my_ip = self.whatismyip()
                self.getPeers()
                for i in self.ip_table.list:
                    if my_ip == i[0]:
                        return i[1]
        except :
            raise "Failed! Check if refresh_table is running. If not call RunService()"


if __name__ == '__main__':
    while True:
        ConnectionHandler()