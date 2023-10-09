import time
import pygame

class Human():
    
    def __init__(self):
        self.kart = None
        
    def move(self, string):
        time.sleep(0.02)
        return pygame.key.get_pressed()