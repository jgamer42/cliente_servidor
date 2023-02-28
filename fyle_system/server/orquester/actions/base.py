from abc import ABCMeta, abstractmethod

from helpers import Index,Config,Conections

class Action(metaclass=ABCMeta):

    def __init__(self,*args,**kwargs):
        self.index = Index()
        self.config = Config()
        self.connections = Conections(list(self.config.data["storers"]))
        
    @abstractmethod
    def execute(self,*args,**kwargs):
        raise NotImplemented