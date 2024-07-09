import json

#region The magic code
import sys
import os
sys.path.insert(0, '{}/../../../'.format(os.getcwd()))
#endregion

class Message :
    def __init__(self , type , format , content):
        self.type = type
        self.format = format
        self.content = content
    
    def to_json(self):
        return {
            "type" : self.type ,
            "format" : self.format,
            "content" : self.content
        }
    
class Text_Message(Message):
    def __init__(self , content):
        self.type = "message"
        self.format = "text"
        self.content = content
