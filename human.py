import time
import pygame
from controller import Controller
from kart import Kart


#this is the class for the human controller. It parses the commanded key and returns it. 

class Human(Controller):
    
    def move(self, string):
        delay = (1./(120.*Kart.nbr_of_karts_()))
        time.sleep(delay)
        super(Human, self.__class__).step.fset(self, super().step+1)
        return pygame.key.get_pressed()
    
    
    def reset(self, step):
        super(Human, self.__class__).step.fset(self, step)
        pass