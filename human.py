import time
import pygame

class Human():
    
    def __init__(self):
        self.kart = None
        self.step = 0
        
    def move(self, string):
        time.sleep(0.02)
        return pygame.key.get_pressed()
    
    def reset(self):
        pass