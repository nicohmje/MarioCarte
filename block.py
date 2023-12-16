from abc import ABC, abstractmethod

class Block(ABC):

    def __init__(self,x,y) -> None:
        self.__rect = None
        pass

    @property
    @abstractmethod
    def surface_type_(self) -> float:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass