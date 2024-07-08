import requests
import json


class IPTable:
    def __init__(self):
        self.list = []
    
    def add_ip(self, address : str):
        if address not in self.list:
            self.list.append(address)
    
    def add_ips(self , addresses:list):
        for i in addresses:
            if i not in self.list:
                self.list.append(i)

    def get_list(self):
        return self.list
    



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
    
    return table

print(getPeers().list)