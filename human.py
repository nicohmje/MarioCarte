import time
import pygame

class Human():
    
    def __init__(self):
        self.__kart = None
        self.is_ai = False

    @property 
    def kart(self):
        return self.__kart
        
    def move(self, string):
        time.sleep(0.01)
        return pygame.key.get_pressed()
    
    def reset(self, step):
        pass