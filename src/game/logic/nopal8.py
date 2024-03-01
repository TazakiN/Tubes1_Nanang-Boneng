import random
from colorama import Fore, Style
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class NopalLogic8(BaseLogic):
    # GREEDY BY DIAMOND
    # akurat cari diamond terdekat
    # kalau inventori udah 4, ketemu diamond point 2 (4 + 2 != 5), maka skip diamond tersebut (cegah error)
    # timing base: detik 46 kalau masih jauh dari base, suruh pulang, kalau dekat dengan base, suruh pulang di detik 53
    # tackle: NONE
    # defense: NONE
    # modularisasi diamond terdekat
    # tackle/defense

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

    
    def closest_diamond(self, board: Board, board_bot: GameObject):
        diamond_position = board.diamonds[0].position
        self.goal_position = diamond_position
        print(f"POSISI diaomon: {diamond_position}")

        # Cari diamond terdekat dari bot
        print(f'DIAMOND COUNT: {len(board.diamonds)}')
        for i in range(1, len(board.diamonds)):
            distance_to_diamond_i = self.distance(board.diamonds[i].position.x, board_bot.position.x, board.diamonds[i].position.y, board_bot.position.y)
            distance_to_diamond = self.distance(diamond_position.x, board_bot.position.x, diamond_position.y, board_bot.position.y)

            # Cegah error inventory penuh
            if board.diamonds[i].properties.points == 2 and board_bot.properties.diamonds == 4:
                print("DIAMOND 2 TAPI UDAH 4")
                continue

            elif distance_to_diamond_i < distance_to_diamond:
                diamond_position = board.diamonds[i].position
                self.goal_position = diamond_position
                diamond_position_new = diamond_position
                print(f"POSISI diaomon NEW: {diamond_position_new} ")
        
        return self.goal_position

    def enemy_bot(self, board: Board,  board_bot: GameObject):
        bot_enemy_position = []
        print(f'BOT Sendiri: {board_bot}')
        print(f'ENEMY COUNT: {len(board.bots)}')
        for bots in board.bots:
            if bots.id != board_bot.id:
                bot_enemy_position.append((bots.position.x, bots.position.y))
        print(f'BOT ENEMY: {bot_enemy_position}')

        our_bot = (board_bot.position.x, board_bot.position.y)
        print(f'OUR BOT: {our_bot}')
        print((board_bot.position.x+1, board_bot.position.y) )
        if (board_bot.position.x + 1, board_bot.position.y) in bot_enemy_position:
            # if board.height
            print(Fore.RED + Style.BRIGHT +"KANAN ADA MUSUH" + Style.RESET_ALL)
            # lakukan gerakan yang valid (tidak menabrak batas height dan widht matrix)
            if board_bot.position.x == 0:
                if board_bot.position.y == 0:
                    print(Fore.BLUE +"SUDAH DI POJOK KIRI ATAS, BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
                elif board_bot.position.y == board.height-1:
                    print(Fore.BLUE +"SUDAH DI POJOK KIRI BAWAH, BERGERAK KE ATAS" + Style.RESET_ALL)
                    return 0, -1
                else:
                    print(Fore.BLUE +"BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE +"BERGERAK KE KIRI" + Style.RESET_ALL)
                return -1, 0

        if (board_bot.position.x - 1, board_bot.position.y) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT +"KIRI ADA MUSUH"+ Style.RESET_ALL)
            if board_bot.position.x == board.width - 1:
                if board_bot.position.y == 0:
                    print(Fore.BLUE +"SUDAH DI POJOK KANAN ATAS, BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
                elif board_bot.position.y == board.height-1:
                    print(Fore.BLUE +"SUDAH DI POJOK KANAN BAWAH, BERGERAK KE ATAS" + Style.RESET_ALL)
                    return 0, -1
                else:
                    print(Fore.BLUE +"BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE +"BERGERAK KE KANAN" + Style.RESET_ALL)
                return 1, 0

        if (board_bot.position.x, board_bot.position.y + 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT +"ATAS ADA MUSUH"+ Style.RESET_ALL)
            if board_bot.position.y == board.height - 1:
                if board_bot.position.x == 0:
                    print(Fore.BLUE +"SUDAH DI POJOK KIRI BAWAH, BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
                elif board_bot.position.x == board.width-1:
                    print(Fore.BLUE +"SUDAH DI POJOK KANAN BAWAH, BERGERAK KE KIRI" + Style.RESET_ALL)
                    return -1, 0
                else:
                    print(Fore.BLUE +"BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE +"BERGERAK KE BAWAH" + Style.RESET_ALL)
                return 0, 1

        if (board_bot.position.x, board_bot.position.y - 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT +"BAWAH ADA MUSUH"+ Style.RESET_ALL)
            if board_bot.position.y == 0:
                if board_bot.position.x == 0:
                    print(Fore.BLUE +"SUDAH DI POJOK KIRI ATAS, BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
                elif board_bot.position.x == board.width-1:
                    print(Fore.BLUE +"SUDAH DI POJOK KANAN ATAS, BERGERAK KE KIRI" + Style.RESET_ALL)
                    return -1, 0
                else:
                    print(Fore.BLUE +"BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE +"BERGERAK KE ATAS" + Style.RESET_ALL)
                return 0, -1
        return None
    
    # def tackle(self, board_bot: GameObject, board: Board):
    #     bot_enemy = board.bots.


    def next_move(self, board_bot: GameObject, board: Board):
        if self.enemy_bot(board, board_bot):
            return self.enemy_bot(board, board_bot)

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
                self.goal_position = self.closest_diamond(board, board_bot)

        else:
            self.goal_position = self.closest_diamond(board, board_bot)
        
        print(f"POSISI BOT: {board_bot.position}")
        print(f"TARGET: {self.goal_position}")

        current_position = board_bot.position
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