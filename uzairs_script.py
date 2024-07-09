import app.src.python.netb as nb
from app.src.python.settings import *
from app.lib.jdata import *

handler = nb.ConnectionHandler()

initial_len = len(handler.stream)

while True:
    if len(handler.stream) > initial_len :
        print(handler.stream)