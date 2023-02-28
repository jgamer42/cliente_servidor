import json
import zmq

#CODE TAKEN FROM 
# https://refactoring.guru/design-patterns/singleton/python/example
class Singelton(type):
    _instances: dict = {}
    """
    Class used as a singelton implementation
    this singelton implementation depends
    of the format that is go to be loaded
    """

    def __call__(self, *args, **kwargs):
        if self.json not in self._instances.keys():
            new_instance = super().__call__(*args, **kwargs)
            self._instances[self.json] = new_instance
        return self._instances[self.json]


class Index(metaclass=Singelton):
    json = "index.json"
    def __init__(self):
        self.load()

    def load(self):
        file = open(f"configs/{self.json}","r")
        data = json.loads(file.read())
        self.data = data
        file.close()
    
    def export(self):
        file = open(f"configs/{self.json}","w")
        file.write(json.dumps(self.data))
        file.close()

class Config(metaclass=Singelton):
    json ="config.json"
    def __init__(self):
        self.load()

    def load(self):
        file = open(f"configs/{self.json}","r")
        data = json.loads(file.read())
        self.data = data
        file.close()
    
    def export(self):
        file = open(f"configs/{self.json}","w")
        file.write(json.dumps(self.data))
        file.close()

class Conections(metaclass=Singelton):
    json = "conections"
    def __init__(self,conections_to_open):
        self.data = {}
        for conection in conections_to_open:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(f"tcp://{conection}")
            self.data[conection] = socket