import json
import netb
import requests

def CommitSettings():
    file='../user/user_settings.json'
    f = open(file)
    
    #Settings to update
    payload = f

    id = netb.whatismyid()

    url = "https://api.netbird.io/api/peers/{}".format(id)
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : "Token {}".format(netb.SERVICE_TOKEN)
    }
    response = requests.request("PUT" , url , headers=headers , data=payload)
    return response.text


    