import app.src.python.netb as nb
from app.src.python.settings import *
from app.src.python.jdata import *

nb.RunServices()
handler = nb.ConnectionHandler()

initial_len = len(handler.stream)

while True:
    if len(handler.stream) > initial_len :
        print(handler.stream)