from app.src.python.netb import *
from app.src.python.settings import *
from app.lib.jdata import *


#Initialise
handler = ConnectionHandler()

#Check what*** functions
print("Your hostname   : "+whatismyhostname())
print("Your netbird IP : "+whatismyip())
print("Your netbird ID : "+whatismyid())

#Send a message to uzair
msg = Text_Message("This is a test")
handler.Send('100.94.16.21' , msg)

#Receive a message from uzair
while True:
    pass
