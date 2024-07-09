from ...lib.jdata import *
from .netb import *
import requests

def CommitSettings():
    file='../user/user_settings.json'
    f = open(file)
    
    #Settings to update
    payload = f

    id = whatismyid()

    url = "https://api.netbird.io/api/peers/{}".format(id)
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : "Token {}".format(SERVICE_TOKEN)
    }
    response = requests.request("PUT" , url , headers=headers , data=payload)
    return response.text


    