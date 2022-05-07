import math
import numpy as np
from params.input_receiver import receive_inputs
from src.pathexplorer import PathExplorer
from src.configurationspace import ConfigurationSpace
from params.heuristics import EUCL_HEURISTIC, MANHTN_HEURISTIC
from src.robot import TurtleBot


def execute_AStar():
    is_input_valid, init_pos, target_pos, orientation, clearance_req = receive_inputs()

    if is_input_valid:
        init_pos = init_pos[0], init_pos[1]
        target_pos = target_pos[0], target_pos[1]

        # parameters of the turtle_bot referred from turtle bot's data sheet
        #t_bot = TurtleBot(radius=(0.354/2), clearance=clearance_req, wheel_rad=(0.076/2), dist_bet_wheels=0.354)
        t_bot = TurtleBot(radius=(0.105), clearance=clearance_req, wheel_rad=(0.033), dist_bet_wheels=0.16)
 
        c_space = ConfigurationSpace(x_limit=(-5, 5), y_limit=(-5,5), radius_of_bot=t_bot.radius, clearance=clearance_req)

        path_explorer = PathExplorer()
        path_params = path_explorer.start_path_planning(t_bot, c_space, EUCL_HEURISTIC, init_pos, target_pos, orientation)
        return path_params



if __name__ == "__main__":
    execute_AStar()

    
        

     

