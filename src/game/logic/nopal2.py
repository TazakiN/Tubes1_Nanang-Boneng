import random
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class NopalLogic2(BaseLogic):
    # GREEDY BY DIAMOND
    # akurat cari diamond terdekat
    # kalau inventori udah 4, ketemu diamond point 2 (4 + 2 != 5), maka skip diamond tersebut (cegah error)
    # timing base: detik 46 kalau masih jauh dari base, suruh pulang, kalau dekat dengan base, suruh pulang di detik 53
    # tackle: NONE
    # defense: NONE

    def __init__(self):
        self.timer_to_base = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0


    def distance(self, x2, x1, y2, y1):
        # hitung jarak antara dua titik
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        base = board_bot.properties.base

        # Monitor jarak bot ke base
        distance_to_base = self.distance(base.x, board_bot.position.x, base.y, board_bot.position.y)
        print(f'BASE DIST: {distance_to_base}')
        
        # Pulang ketika inventory penuh
        if props.diamonds == 5:
            self.goal_position = base # Base(y=10, x=3)
            
        # Base timing management
        elif self.timer_to_base >= 46:
            if distance_to_base > 5:
                print("TOO FAR")
                self.goal_position = base
            elif self.timer_to_base >= 53:
                print("timer hit")
                self.goal_position = base
            else:
                print("BELUM WAKTUNYA BALIK")

        else:
            # Inisiasi posisi diamond pertama
            diamond_position = board.diamonds[0].position
            self.goal_position = diamond_position
            print("POSISI diaomon: ")
            print(diamond_position)

            # Cari diamond terdekat dari bot
            print(f'DIAMOND COUNT: {len(board.diamonds)}')
            for i in range(1, len(board.diamonds)):
                print(f'ALL DIAMOND: {board.diamonds[i].position}')
                if self.distance(board.diamonds[i].position.x, board_bot.position.x, board.diamonds[i].position.y, board_bot.position.y) < self.distance(diamond_position.x, board_bot.position.x, diamond_position.y, board_bot.position.y):
                    if board.diamonds[i].properties.points == 2 and props.diamonds == 4:
                        print("DIAMOND 2 TAPI UDAH 4")
                        continue
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

            # if delta_x == delta_y:
            #     print("X SAMA Y SAMA")
            #     step = random.randint(-1, 1)
            #     delta_x = step
            #     if delta_y == delta_x:
            #         if delta_x == 0:
            #             delta_y = 1
            #         else :
            #             delta_y = delta_x*-1

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