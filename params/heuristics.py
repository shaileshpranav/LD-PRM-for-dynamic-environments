import math

NO_HEURISTIC = lambda postion, target_pos: 0
EUCL_HEURISTIC = lambda postion, target_pos: math.sqrt((postion[0] - target_pos[0])**2 + (postion[1] - target_pos[1])**2)