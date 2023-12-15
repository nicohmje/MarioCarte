import time
from ai_parse import AI_PARSE
import logging

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

logger = logging.getLogger('MariooCarteLogger')

class AI():
    
    def __init__(self, string, pos_ini, angle_ini):
        self.__kart = None
        self.is_ai = True
        self.__ai = AI_PARSE(string,pos_ini, angle_ini)
        if (AI_PARSE.need_to_map):
            self.__ai.parse()
        else:
            logger.debug("No need to map")
        self.__step = 0

    @property 
    def kart(self):
        return self.__kart
    
    @property 
    def ai(self):
        return self.__ai
    
    @property
    def step(self):
        return self.__step

    def reset(self, step=0):
        self.__step = step

    def move(self, string):
        time.sleep(0.01)
        logger.debug("Step %i", self.__step)
        keys = self.__ai.move(self.__step)
        self.__step+=1
        return keys
        