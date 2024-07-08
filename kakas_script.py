import app.src.python.netb as nb
from app.src.python.settings import *
from app.src.python.jdata import *


#Initialise
nb.RunServices()
handler = nb.ConnectionHandler()

#Send a message to uzair
msg = Text_Message("This is a test")
handler.Send('100.94.16.21' , msg)

#Receive a message from uzair
while True:
    pass;
