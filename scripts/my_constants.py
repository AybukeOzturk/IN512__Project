__author__ = "Aybuke Ozturk Suri, Johvany Gustave"
__copyright__ = "Copyright 2023, IN512, IPSA 2023"
__credits__ = ["Aybuke Ozturk Suri", "Johvany Gustave"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"

""" This file contains all the 'constants' shared by all the scripts """

""" MSG HEADERS """
BROADCAST_MSG = 0
GET_DATA = 1    #get the current location of the agent and the dimension of the environment (width and height)
MOVE = 2
GET_NB_CONNECTED_AGENTS = 3
GET_NB_AGENTS = 4
GET_ITEM_OWNER = 5

""" ALLOWED MOVES """
STAND = 0   #do not move
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
UP_LEFT = 5
UP_RIGHT = 6
DOWN_LEFT = 7
DOWN_RIGHT = 8

""" BROADCAST TYPES """
KEY_DISCOVERED = 1  #inform other agents that you discovered a key
BOX_DISCOVERED = 2
COMPLETED = 3   #inform other agents that you discovered your key and you reached your own box

""" GAME """
GAME_ID = -1    #id of the game when it sends a message to an agent
KEY_NEIGHBOUR_PERCENTAGE = 0.5  #value of an adjacent cell to a key
BOX_NEIGHBOUR_PERCENTAGE = 0.6  #value of an adjacent cell to a key
KEY_TYPE = 0    #one of the types of item that is output by the 'Get item owner' request
BOX_TYPE = 1

""" GUI """
BG_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)