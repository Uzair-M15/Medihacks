
import requests
import socket
from multiprocessing import Process
import json
import asyncio
import os
import subprocess
from platform import system







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
    
    def set_list(self , other : list):
        '''This method should only be used by the netb getPeer method. Turn back. Using it could break EVERYTHING'''
        self.list = []
        for i in other :
            self.list.append(i)

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
            table_string = table_string + '\n' + i[0] + ':' + i[1] +':'+ i[2]
        
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
            if ip==i[0]:
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
        self.server_sock.bind(( self.whatismyip() ,PORT))
        self.max_connections = 50




        #CLIENT CODE
        self.client_sock = socket.socket()



        #storing communication
        self.stream = []

        self.handler_process = Process(target=self.ProcessRunner)
        self.handler_process.daemon = True
        self.handler_process.start()

        #used for communicating between processes
        self.parent_process_sock = socket.socket()
        self.child_process_sock = socket.socket()
        self.parent_process_sock.bind(('localhost' , 8009))
        asyncio.run(self.parent_sync_parent_variables())

        try :
            f = open("app/user/prev_session" , "r")
            prev_ip_table = f.readlines()
            if len(prev_ip_table) != 0:
                for entry in prev_ip_table :
                    values = entry.split(":")
                    prev_sessions_hostname = values[1]
                    prev_sessions_ip = values[1]
                    for item in self.ip_table.list :
                        if item[0] == prev_sessions_ip and item[1] != prev_sessions_hostname:
                            try :
                                os_name = system()
                                os.rename(f"app/chats/{prev_sessions_hostname}" , f"app/chats/{item[1]}")
                                if os_name == 'Windows':
                                    subprocess.Popen(f"ren app/chats/{item[1]}/{prev_sessions_hostname}.txt {item[1]}.txt" , shell=True)
                                elif os_name == 'Linux':
                                    subprocess.Popen(f"mv app/chats/{item[1]}/{prev_sessions_hostname}.txt app/chats/{item[1]}/{item[1]}.txt" , shell= True)  
                            except:
                                pass

        except FileNotFoundError:
            f = open("app/user/prev_session" , "x")
            f.close()

    








    async def parent_sync_parent_variables(self):
        '''Syncs variables betwee spawned child process and parent process.\n Allows data transmission between parent and child'''
        self.parent_process_sock.listen()
        conn , address = self.parent_process_sock.accept()
        message = conn.recv(BUFFER_SIZE).decode()
        message = message.split("\n")
        update_to = message[0]
        message.pop(0)

        i = 0
        if update_to == "ip_table":
            for line in message:
                split_line = line.split(":")
                message[i] = (split_line[0] , split_line[1] , split_line[2])
                i = i + 1
            
            self.ip_table.set_list(message)
        elif update_to == "stream":
            self.stream.append(message[0])



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
    








    def Receive(self , address , sock):
        #add implementation for notifications
        print("Preparing to receive message from {}".format(address))
        message = sock.recv(BUFFER_SIZE)
        message = message.decode()
        
        #Transmit data from child to parent
        self.child_process_sock = socket.socket()
        self.child_process_sock.connect(('localhost' , 8009))
        self.child_process_sock.send(("stream\n"+message).encode())
        self.child_process_sock.close()
        
        if message != "":
            #handling input
            message = json.loads(message)
            if message["type"]=="message":
                host = self.ip_table.get_hostname(address)
                try:
                    chat = open(f'app/chats/{host}/{host}.txt' , "a")
                    chat.write(str(message))
                    chat.close()
                except FileNotFoundError :
                    chat = open(f'app/chats/{host}/{host}.txt' , 'x')
                    chat.close()
                    chat = open(f'app/chats/{host}/{host}.txt' , 'a')
                    chat.write(str(message))
                    chat.close()
            if message["type"] == "host_update_message":
                old_host = message["content"].split(":")[0]
                new_host = message["content"].split(":")[1]
                try :
                    os_name = system()
                    if os_name == 'Windows':
                        subprocess.Popen(f"ren app/chats/{old_host}.txt {new_host}.txt" , shell=True)
                    elif os_name == 'Linux':
                        subprocess.Popen(f"mv app/chats/{old_host}.txt app/chats/{new_host}.txt" , shell= True)        
                except: 
                    pass






    async def AcceptConnection(self):
        print("Starting Connect Acceptions")
        #Implement IP Blocking
        while True :
            self.server_sock.listen()
            conn,address = self.server_sock.accept()
            
            print("Connection Accepted for address :{}".format(address[0]))
            self.Receive(address=address[0] , sock = conn)

    #endregion
    
    #region client_sock code

    def Connect(self , address):
        '''Connects to an address. Should not be called. The Send method handles connection'''
        try:
            self.client_sock.connect((address, PORT))
            print("Connected to peer")
            return 0
        except Exception as e:
            return 0
    






    def Send(self , address , message):
        print("Trying to send message:{}".format(message.to_string()))
        try:
            self.client_sock = socket.socket()
            self.Connect(address=address)
            self.client_sock.send(message.to_string().encode())
            #if self.client_sock.recv(BUFFER_SIZE).decode() == message.to_string():
            self.client_sock.close()


            try:
                host = self.ip_table.get_hostname(address)
                me = self.whatismyhostname()
                chat = open(f'app/chats/{host}/{me}.txt' , "a")
                chat.write(str(message))
                chat.close()
            except FileNotFoundError :
                chat = open(f'app/chats/{host}/{me}.txt' , 'x')
                chat.close()
                chat = open(f'app/chats/{host}/{me}.txt' , 'a')
                chat.write(str(message))
                chat.close()
            #else:
             #   print("Cant send message to address:{}".format(address))
              #  print("Possible Error due to existing connection. Message will not be sent and transmission socket will be closed")
               # self.client_sock.close()
        except:
            raise Exception("Message might not be a valid jdata.Message object. Cancelling")

    #endregion








    def ProcessRunner(self):
        print('\nChild process started with id:{}'.format(os.getpid()))
        print("This process' Parent id :{}".format(os.getppid()))
        while True:
            self.getPeers()
            asyncio.run(self.AcceptConnection())








    #Update IP table
    def getPeers(self)->IPTable:
        '''Refreshes the ConnectionHandler.ip_table . 
        \n[!]It should not be called by anything other than the ProcessRunner process. 
        \nCalling it might have no effect at all but it would be redundant (in a best case scenario) and may result in unexpected or incorrect output'''
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
        
        self.ip_table.set_list(table.list)
        self.client_sock.connect(('localhost' , 8009))
        self.client_sock.send(("ip_table"+self.ip_table.__str__()).encode())
        self.client_sock.close()
        print("[=] Update to IP Table :\n"+self.ip_table.__str__())

        f = open('app/user/prev_session' , 'w')
        f.write("")
        f.close

        for i in self.ip_table.list :
            try :
                f = open("app/user/prev_session" , 'a')
                f.write(f"{i[0]}:{i[1]}:{i[2]}")
                f.close()
            except FileNotFoundError :
                pass








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
            for i in self.ip_table.list:
                if i[0] == my_ip:
                    return i[2]
        except :
            raise "Failed! Check if refresh_table process is running. If not call RunService()"







    def whatismyhostname(self)->str:
        '''Returns the users netbird hostname'''
        try:        
                my_ip = self.whatismyip()
                for i in self.ip_table.list:
                    if my_ip == i[0]:
                        return i[1]
        except :
            raise "Failed! Check if refresh_table is running. If not call RunService()"








    def CommitSettings(self):
        '''Edit json to support payload'''
        #broadcast update

        file='app/user/user_settings.json'
        f = open(file , 'r')

        hostname_changed = json.load(f)["netbird"]["name"] == self.whatismyhostname()

        if hostname_changed :
            message = {
                    "type" : "host_update_message",
                    "format" : "text",
                    "content" : f"{self.whatismyhostname()}:{f.readlines()[1]}"
                }
            for i in self.ip_table.IPs():
                self.Send(i , message=message)
        f.close()



        #Update settings
        f = open("app/user/user_settings.json")
        payload = json.load(f)
        payload = payload["netbird"]
        f.close()
        id = self.whatismyid()

        url = "https://api.netbird.io/api/peers/{}".format(id)
        headers = {
            "Content-Type" : "application/json" ,
            "Accept" : "application/json",
            "Authorization" : "Token {}".format(SERVICE_TOKEN)
        }
        response = requests.request("PUT" , url , headers=headers , data=payload)




    def ChangeSetting(self , setting_name , setting_value , commit:bool = True):
        '''Edit user settings'''
        f = open('app/user/user_settings.json')
        data = json.load(f)
        f.close()

        for i in data['netbird']:
            for key in i :
                if key == "id":
                    data['netbird']['id'] = self.whatismyid()
                if key == "name":
                    data['netbird']['name'] = self.whatismyhostname()
                if key == setting_name :
                    data['netbird'][setting_name] = setting_value
        
        json.dump(data , open('app/user/user_settings.json' , "w"))

        if commit :
            self.CommitSettings()
    




    def Close(self):
        self.handler_process.kill()
        self.parent_process_sock.close()
        exit()
                
if __name__ == '__main__':
    import jdata

    handler = ConnectionHandler()
    message = jdata.Text_Message("This is another test")
    handler.Send(handler.whatismyip() , message)
    handler.ChangeSetting("name" , "uzairs_kali_machine")
    handler.Close()
