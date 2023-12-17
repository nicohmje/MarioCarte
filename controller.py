from abc import ABC, abstractmethod


class Controller(ABC):

    def __init__(self):
        self.__kart = None
        self.is_ai = False
        self.__step = 0


    @property 
    def kart(self):
        return self.__kart
    
    @property 
    def step(self):
        return self.__step
    
    @step.setter
    def step(self, value):
        self.__step = value
        pass


    @abstractmethod
    def move(self, string):
        pass

    @abstractmethod
    def reset(self, step=0):
        pass