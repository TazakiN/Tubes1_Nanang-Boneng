import random
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
from time import time

class NopalLogic2(BaseLogic):
    # def timer(seconds):
    #     start_time = time()
    #     while True:
    #         elapsed_time = time() - start_time
    #         print(f'Timer: {elapsed_time}')
    #         if elapsed_time >= seconds:
    #             break
    #     return True
    
    # timer_to_base = timer(10)

    def __init__(self):
        self.timer_to_base = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0


    # def distance(self, x2, x1, y2, y1):
    #     return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        base = board_bot.properties.base

        # distance_to_base = self.distance(base.x, board_bot.position.x, base.y, board_bot.position.y)
        # print(f'BASE DIST: {distance_to_base}')
        # too_far = False
        # print(f'too far?: {too_far}')
        # if distance_to_base > 5:
        #     too_far = True

        if props.diamonds == 5:
            # Move to base
            self.goal_position = base # Base(y=10, x=3)
            
        
        # elif self.timer_to_base >= 46 and too_far:
        elif self.timer_to_base >= 46:
            print("timer hit")
            self.goal_position = base

        else:
            # Just roam around
            # self.goal_position = None

            diamond_position = board.diamonds[0].position
            self.goal_position = diamond_position
            print("POSISI diaomon: ")
            print(diamond_position)

            # diamond terdekat dari bot
            print(f'DIAMOND COUNT: {len(board.diamonds)}')
            for i in range(1, len(board.diamonds)):
                print(f'ALL DIAMOND: {board.diamonds[i].position}')
                if (board.diamonds[i].position.x - board_bot.position.x) + (board.diamonds[i].position.y - board_bot.position.y) < (diamond_position.x - board_bot.position.x) + (diamond_position.y - board_bot.position.y):
                    diamond_position = board.diamonds[i].position
                    self.goal_position = diamond_position
                    diamond_position_new = diamond_position
            print("POSISI diaomon NEW: ")
            print(diamond_position_new)
            
                

        current_position = board_bot.position
        print("POSISI bot: ")
        print(current_position)
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

            if delta_x == delta_y:
                print("X SAMA Y SAMA")
                step = random.randint(-1, 1)
                delta_x = step
                if delta_y == delta_x:
                    if delta_x == 0:
                        delta_y = 1
                    else :
                        delta_y = delta_x*-1

        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )

        # print("POSISI diaomon: ")
        # print(board.diamonds[0].position.x)

        # print("ALL DIAMONDS: ")
        # print(board.diamonds)

        self.timer_to_base += 1
        print(f'timer: {self.timer_to_base}')
        return delta_x, delta_y