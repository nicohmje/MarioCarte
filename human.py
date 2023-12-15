import time
import pygame


#this is the class for the human controller. It parses the commanded key and returns it. 

class Human():
    
    def __init__(self):
        self.__kart = None
        self.is_ai = False
        self.step = 0

    @property 
    def kart(self):
        return self.__kart
        
    def move(self, string):
        time.sleep(0.005)
        return pygame.key.get_pressed()
    
    def reset(self, step):
        pass