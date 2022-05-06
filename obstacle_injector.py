import time
from constants import DONE, MOVING
from math import sin


def obstacle_injector(task_status, bot_status, c_space):
    obstacles = [
        
        [(0.5+c_space.padding), [-2,4]], 
        # [(0.2+c_space.padding), (3, 2)],
        [(0.3+c_space.padding), [4,-2]],
        
        # [(0.4+c_space.padding), (4,-1)],
        [(0.5+c_space.padding), [2, -3]],
        # [(0.5+c_space.padding), [-2,2.5]],
        # [(0.6+c_space.padding), (-3, 3)]
    ]

    i = 0
    sleep_time = 0
    while not task_status[DONE]:
        # time.sleep(sleep_time)
        if not task_status[DONE]:
            if bot_status[MOVING]:
                # c_space.obstacle_list.pop(-1)
                # obstacles[0][1][0]=0.4+sin(i/5)
                obstacles[0][1][1]-=0.07
                obstacles[1][1][0]-=0.05
                obstacles[2][1][1]+=0.1
                c_space.obstacle_list[0][1][1]+=0.05
                c_space.obstacle_list.append(obstacles[0])
                c_space.obstacle_list.append(obstacles[1])
                c_space.obstacle_list.append(obstacles[2])
                # c_space.obstacle_list.append(obstacles[3])
                bot_status[MOVING] = False
                print('New obstacle added.')
                i += 1
                sleep_time = 0.01
        
    print('Task Done')
        

