import requests
import socket
import asyncio
import json
import subprocess
import jdata

ip_table = None
PORT= 8008
BUFFER_SIZE = 4096
SERVICE_TOKEN = 'nbp_uhFD8nKYULoPNz6WZlKoY34LxRBv9B0nt3Fv'

class ConnectionHandler:
    '''Asyncronously manages connection processes (Sending, Receiving)'''
    def __init__(self):
        #SERVER CODE
        #[( address , socket object ) , ...]
        self.connected_peers = []
        self.ip = whatismyip()

        #local server
        self.server_sock = socket.socket()
        self.server_sock.bind(('localhost' ,PORT))

        #CLIENT CODE
        self.client_sock = socket.socket()



        #storing communication
        self.stream = []

        asyncio.run(self.AcceptConnection)

    #region server_sock code
    def GetSock(self , address)->socket.socket:
        for i in self.connected_peers :
            if i[0] == address:
                return i[1]
        raise Exception("Socket Object not found for address : {}".format(address))

    def ServerSend(self,address , message:jdata.Message):
        msg = {
            "type":message.type,
            "format":message.format,
            "content":message.content,
            "to" : address,
            "from" : whatismyip()
        }
        msg = json.dumps(msg)
        self.stream.append(msg)
        self.GetSock(address).send(msg.encode())
    
    async def Receive(self , address):
        #add implementation for notifications
        sock = self.GetSock(address)
        message = sock.recv(BUFFER_SIZE)
        message = message.decode()
        self.stream.append(message)
        print(message)

        #handling input
        message = json.loads(message)
        if message["type"]=="message":
            host = ip_table.get_hostname(address)
            chat = open('../chats/{}.txt'.format())
            chat.write(message)

    async def AcceptConnection(self):
        while True :
            self.server_sock.listen()
            conn,address = self.server_sock.accept()
            self.connected_peers.append(address[0] , conn)
            print("Connection Accepted for address :{}".format(address[0]))
            asyncio.run(self.Receive(address=address))
            
    #endregion
    

    #region client_sock code

    def Connect(self , address):
        try:
            self.client_sock.connect((address, PORT))
            return 0
        except:
            print("An error occured while connecting")
            return 1
    
    def Disconnect(self):
        self.client_sock.close()
    
    def Send(self , address , message:jdata.Message):
        if self.Connect(address)== 0:
            message = {
                "type":message.type, 
                "format" : message.format,
                "to" : address , 
                "from" : whatismyip(),
                "content" : message.content
            }
            self.client_sock.send("")
        else:
            print("Cant send message to address:{}".format(address))

    #endregion

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


#Update IP table
async def getPeers()->IPTable:
    while True:
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
        
        ip_table = table

def whatismyip()->str:
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
            return ip

def whatismyid()->str:
    '''Returns the users netbird id'''
    my_ip = whatismyip()
    for i in ip_table:
        if i[0] == my_ip:
            return i[2]

def whatismyhostname()->str:
    '''Returns the users netbird hostname'''
    
    my_ip = whatismyip()

    for i in ip_table:
        if my_ip == i[0]:
            return i[1]

def RunServices():
    asyncio.run(getPeers)

RunServices()