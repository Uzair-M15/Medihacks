import app.src.python.netb as netb
import app.src.python.ark as ark
import os
import json

handler = netb.ConnectionHandler()
am_i_connected = False
active_chat = ''

def test_function(a:list) :
    a = int(a[0])
    return (a*a)

def initialise(a:list=[]):
    handler = netb.ConnectionHandler.__init__(handler)
    am_i_connected = True
    return ''

def my_id(a:list = []):
    return handler.whatismyid()

def my_ip(a:list = []):
    return handler.whatismyip()

def my_hostname(a:list = []):
    try:
        return handler.whatismyhostname()
    except:
        return 'There was an error with your nest script'

def getSpecialChars(a:str):
    special_chars = [] 
    a = a[0]
    special_chars.append(a[0])

    for letter in a :
        if letter.isupper():
            special_chars.append(letter)
        if letter.isnumeric():
            special_chars.append(letter)
    
    return "".join(special_chars)

def SendPageSetup(a:list = []):
    page = ""
    for i in handler.ip_table.list :
        page = page + f'<a href="http://127.0.0.1:808/send/user/{i[1]}" style="text-decoration:none;"><div class = "box-border"><div class = "user-label">{getSpecialChars([i[1]])}</div><div class="user-details">Hostname   : {i[1]}<br>IP Address : {i[0]}</div></div></a><br>'

    return page

def getMessages(a:list = []):
    directory = f"app/chats/{active_chat}"

    try : 
        sent = f"{directory}/me.txt"
        received = f"{directory}/{active_chat}.txt"

        ark.sort(sent , received , directory )

    except:
        return ""
    
    try:
        with open(directory+"/sorted.txt" , "r") as file :
            out = "" 
            for i in file.readlines() :
                message = i.removeprefix("".join(i[0:i.index("]")+1]))
                message = message.removesuffix("\n")
                message = message.replace("'" , '"')
                message = message.replace("%21" , " ")
                

                message = json.loads(message)

                if message["sent"] == "True":
                    out = out + f'<div class="sent-message">{message["content"]}</div><br>'
                elif (not message["sent"] == "False"):
                    out = out + f'<div class="received-message">{message["content"]}</div><br>'
                else: return 'An error occured with processing your messages'
            
        return out
    
    except FileNotFoundError :
        return ''

def getSendFormAction(a:list = []):
    return f'"http://127.0.0.1:808/send/user/{active_chat}"'

namespace = {
    "function":{
        "test_function" : test_function,
        "my_id" : my_id , 
        "my_ip" : my_ip ,
        "my_hostname" : my_hostname ,
        "SpecialChars" : getSpecialChars,
        "setup_send_page" : SendPageSetup,
        "populate_chat" : getMessages ,
        "get_send_form_action" : getSendFormAction,
    } ,
    "variable":{
        "test_var" : 5,
        "connected" : am_i_connected,
        
    },
}

components = {
    
}