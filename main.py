from track import Track
from ai import AI
from human import Human
from kart import Kart
import logging


logging.basicConfig(level=logging.INFO, format='%(filename)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('MariooCarteLogger')


# La chaine de caractere decrivant le terrain

# string = """RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR"""


string = """GGGGGGGGGGGGGGGGGGGGGGGGGG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGRRRRG
GFFRRGGGGGGGGGGGGGGGGRRRRG
GLRRRGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGDDDDG
GRRRLRRRERRRRRRRRRRRRRRLLG
GRRRLRRRERRRRRRRRRRRRRRRRG
GRRRRRRRERRRGGRRRRRRRRRRRG
GRRRRRRRERRRGGRRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGGGGGG"""


# La position et l'orientation initiale du kart
initial_position = [150., 150.]
initial_angle = 0.

controller_2 =  Human(initial_position, initial_angle)  # ou AI()
# controller = AI(string,initial_position, initial_angle)

"""
==================== ATTENTION =====================
Vous ne devez pas modifier ces quatre lignes de code 
====================================================
"""

kart = Kart(controller_2)
track = Track(string, initial_position, initial_angle)
track.add_kart(kart)
track.play()