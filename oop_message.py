import json

class Message:
    @staticmethod
    def move(x, y):
        return json.dumps({
            'type': 'move',
            'payload': {
                'x': x,
                'y': y
            }
        }).encode('utf-8')
    
    @staticmethod
    def chat(msg):
        return json.dumps({
            'type': 'chat',
            'payload': msg
        }).encode('utf-8')
    
    @staticmethod
    def flag(flag):
        return json.dumps({
            'type': 'flag',
            'payload': flag
        }).encode('utf-8')
