import random
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class NopalLogic6(BaseLogic):
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
    

    def red_diamonds(self, board: Board):
        # list diamond merah
        return [d for d in board.game_objects if d.properties.points == 2]


    def get_teleporter(self, board: Board) -> Optional[Position]:
        return [t for t in board.game_objects if t.type == "TeleportGameObject"]

    
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
            elif self.timer_to_base >= 52:
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
                red_diamond = self.red_diamonds(board)
                red_diamond_count = len(red_diamond)
                # print(f'ALL DIAMOND: {board.diamonds[i].position}')
                # print(f'RED DIAMOND: {red_diamond}')

                # j = 0
                # red_diamond_position = None
                # if j < red_diamond_count:
                #     red_diamond_position = red_diamond[j].position
                #     print(f'RED DIAMOND: {red_diamond[j].position}')
                #     j += 1
                
                distance_to_diamond_i = self.distance(board.diamonds[i].position.x, board_bot.position.x, board.diamonds[i].position.y, board_bot.position.y)
                distance_to_diamond = self.distance(diamond_position.x, board_bot.position.x, diamond_position.y, board_bot.position.y)

                # Cegah error inventory penuh
                if board.diamonds[i].properties.points == 2 and props.diamonds == 4:
                    print("DIAMOND 2 TAPI UDAH 4")
                    continue

                # Diamond terdekat dari bot
                # if red_diamond_position:
                #     distance_to_red_diamond = self.distance(red_diamond_position.x, board_bot.position.x, red_diamond_position.y, board_bot.position.y)
                #     print(f'DIST RED: {distance_to_red_diamond}')
                #     if distance_to_diamond_i <= 1:
                #         print(f'DISTANCE TO RED DIAMOND: {distance_to_red_diamond}')
                #         self.goal_position = red_diamond_position
                #         print("POSISI diaomon RED: ")
                #         print(red_diamond_position)

                elif distance_to_diamond_i < distance_to_diamond:
                    diamond_position = board.diamonds[i].position
                    self.goal_position = diamond_position
                    diamond_position_new = diamond_position
                    print("POSISI diaomon NEW: ")
                    print(diamond_position_new)
                
        print(f"TARGET: {self.goal_position}")

        teleporter = self.get_teleporter(board)
        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            
            # for t in teleporter:
            #     if self.distance(current_position.x, t.position.x, current_position.y, t.position.y) <= 1:
            #         print("TELEPORTER")
            #         delta_x = 0
            #         delta_y = 1

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