import random
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class NopalLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base # Base(y=10, x=3)
            

        else:
            # Just roam around
            # self.goal_position = None
            diamond_position = board.diamonds[0].position
            self.goal_position = diamond_position
            print("POSISI diaomon: ")
            print(diamond_position)

            # diamond terdekat dari 0,0
            # for i in range(1, len(board.diamonds)):
            #     if board.diamonds[i].position.x + board.diamonds[i].position.y < diamond_position.x + diamond_position.y:
            #         diamond_position = board.diamonds[i].position
            #         self.goal_position = diamond_position
            #         print("POSISI diaomon NEW: ")
            #         print(diamond_position)

            # diamond terdekat dari bot
            for i in range(1, len(board.diamonds)):
                if (board.diamonds[i].position.x - board_bot.position.x) + (board.diamonds[i].position.y - board_bot.position.y) < (diamond_position.x - board_bot.position.x) + (diamond_position.y - board_bot.position.y):
                    diamond_position = board.diamonds[i].position
                    self.goal_position = diamond_position
                    print("POSISI diaomon NEW: ")
                    print(diamond_position)
                    
                

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

            # if delta_x == 0 and delta_y == 0:
            #     self.goal_position = board.diamonds[1].position

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

        print("ALL DIAMONDS: ")
        print(board.diamonds)


        return delta_x, delta_y