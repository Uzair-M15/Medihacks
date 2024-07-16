import json
import datetime

class Message :
    def __init__(self , type , format , content , sent = "False"):
        self.type = type
        self.format = format
        self.content = content
        self.sent = sent
        self.timestamp = ""
    
    def stamp(self):
        dt = datetime.datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        seconds = dt.second
        millisecond = str(dt.microsecond)[0] + str(dt.microsecond)[1]
        

        self.timestamp = f'[{millisecond}:{seconds}:{minute}:{hour}:{day}:{month}:{year}]'
    
    def to_json(self)->json:
        return {
            "type" : self.type ,
            "format" : self.format,
            "content" : self.content ,
            "sent" : self.sent ,
            "timestamp" : self.timestamp
        }

    def to_string(self)->str:
        return json.dumps(self.to_json())
    
class Text_Message(Message):
    def __init__(self , content , sent="False"):
        self.type = "message"
        self.format = "text"
        self.content = content
        self.sent = sent
        self.timestamp = ""