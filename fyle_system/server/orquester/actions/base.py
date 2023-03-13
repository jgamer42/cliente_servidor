from abc import ABCMeta, abstractmethod

from helpers import Index,Config

class Action(metaclass=ABCMeta):

    def __init__(self,*args,**kwargs):
        self.index = Index()
        self.config = Config()
        
    @abstractmethod
    def execute(self,*args,**kwargs):
        raise NotImplemented