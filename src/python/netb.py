import requests
import socket
import asyncio
import json

ip_table = None
port = 8008

class ConnectionHandler:
    '''Asyncronously manages connection processes (Sending, Receiving)'''
    def __init__(self):
    #SERVER CODE
        #[( address , socket object ) , ...]
        self.connected_peers = []

        #local server
        self.server_sock = socket.socket()
        self.server_sock.bind(('localhost' ,port))
        
        #storing communication
        self.stream = []
    

    #region server_sock code
    def GetSock(self , address)->socket.socket:
        for i in self.connected_peers :
            if i[0] == address:
                return i[1]
        raise Exception("Socket Object not found for address : {}".format(address))

    def ServerSend(self,address , message):
        msg = {
            "type":"server_message",
            "content":message
        }
        self.GetSock(address).send(json.dumps(msg).encode())

    async def AcceptConnection(self):
        while True :
            self.server_sock.listen()
            conn,address = self.server_sock.accept()
            self.connected_peers.append(address[0] , conn)
            print("Connection Accepted for address :{}".format(address[0]))
            self.ServerSend(address[0] , 'Connection Succeeded')
    #endregion
    


class IPTable:
    def __init__(self):
        self.list = []
    
    def add_address(self, ip : str , hostname:str):
        if ip not in self.list:
            self.list.append((ip , hostname))
        else:
            print("Address already exists. Ignoring")

    def get_list(self):
        return self.list

    def hostnames(self):
        hosts = []
        for i in self.list:
            hosts.append(i[1])
        
        return hosts
    
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
        for i in self.list:
            if hostname == i[1]:
                return i[0]
    
    def get_hostname(self , ip):
        for i in self.list:
            if ip == i[0]:
                return i[1]



def getPeers():
    service_token = 'nbp_uhFD8nKYULoPNz6WZlKoY34LxRBv9B0nt3Fv'
    headers = {
        'Accept' : 'application/json' ,
        'Authorization': 'Token {}'.format(service_token)
        }
    response = requests.request('get' ,'https://api.netbird.io/api/peers' , headers=headers)
    response=response.json()
    #Make IP Table
    table = IPTable()

    for i in response:
        table.add_ip(i["ip"])
