import time
import pygame

class Human():
    
    def __init__(self):
        self.kart = None
        self.is_ai = False
        self.step = 0
        
    def move(self, string):
        time.sleep(0.01)
        return pygame.key.get_pressed()
    
    def reset(self, step):
        pass