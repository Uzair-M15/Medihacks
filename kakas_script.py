from app.src.python.netb import *
from app.src.python.settings import *
from app.src.python.jdata import *


#Initialise
handler = ConnectionHandler()

#Send a message to uzair
msg = Text_Message("This is a test")
handler.Send('100.94.16.21' , msg)

#Receive a message from uzair
while True:
    pass
