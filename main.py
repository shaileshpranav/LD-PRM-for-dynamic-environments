import math
import numpy as np
from params.input_receiver import readInputs
from src.pathExplorer import PathPlanner
from src.cspace import ConfigurationSpace
from params.heuristics import EUCL_HEURISTIC, MANHTN_HEURISTIC
from src.robot import Robot


def main():
    isValid, start_pos, target_pos, orientation, clearance = readInputs()

    if not isValid: return None

    start_pos = start_pos[0], start_pos[1]
    target_pos = target_pos[0], target_pos[1]

    # parameters of the turtle_bot referred from turtle bot's data sheet
    bot = Robot(radius=(0.105), clearance=clearance, wheel_rad=(0.033), dist_bet_wheels=0.16)

    c_space = ConfigurationSpace(x_limit=(-5, 5), y_limit=(-5,5), radius_of_bot=bot.radius, clearance=clearance)

    planner = PathPlanner()
    planner_results = planner.plan(bot, c_space, EUCL_HEURISTIC, start_pos, target_pos, orientation)
    return planner_results



if __name__ == "__main__":
    main()

    
        

     

