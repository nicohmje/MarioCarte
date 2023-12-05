import time
from radar import AI_PARSE
import logging

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

logger = logging.getLogger('MariooCarteLogger')

class AI():
    
    def __init__(self, string, pos_ini, angle_ini):
        self.kart = None
        self.is_ai = True
        self.ai = AI_PARSE(string,pos_ini, angle_ini)
        if (AI_PARSE.need_to_map):
            self.ai.parse()
        else:
            logger.debug("No need to map")
        self.step = -1

    def reset(self, step=-1):
        self.step = step

    def move(self, string):
        self.step += 1
        time.sleep(0.02)
        return self.ai.move(self.step)