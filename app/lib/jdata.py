import json
#region The magic code
import sys
import os
#endregion

class Message :
    def __init__(self , type , format , content):
        self.type = type
        self.format = format
        self.content = content
    
    def to_json(self)->json:
        return {
            "type" : self.type ,
            "format" : self.format,
            "content" : self.content
        }

    def to_string(self)->str:
        self.to_json().dumps()
    
class Text_Message(Message):
    def __init__(self , content):
        self.type = "message"
        self.format = "text"
        self.content = content
