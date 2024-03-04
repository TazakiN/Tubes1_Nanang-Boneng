import random
from colorama import Fore, Style
from typing import Optional, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class TeleLogic(BaseLogic):
    # GREEDY BY DIAMOND, TACKLE/DEFENSE, TIMING, AVOID TELEPORT
    # akurat cari diamond terdekat
    # kalau inventori udah 4, ketemu diamond point 2 (4 + 2 != 5), maka skip diamond tersebut (cegah error)
    # timing base: detik 46 kalau masih jauh dari base, suruh pulang, kalau dekat dengan base, suruh pulang di detik 53
    # modularisasi diamond terdekat
    # defense: defense_from_enemy
    # tackle: tackle_enemu

    def __init__(self):
        self.timer_to_base = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.sequenceMove = []

    def distance(self, x2, x1, y2, y1):
        # hitung jarak antara dua titik
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def red_diamonds(self, board: Board):
        # list diamond merah
        return [d for d in board.game_objects if d.properties.points == 2]

    def get_teleporter(self, board: Board):
        return [t for t in board.game_objects if t.type == "TeleportGameObject"]

    def closest_diamond(self, board: Board, board_bot: GameObject):
        diamond_position = board.diamonds[0].position
        self.goal_position = diamond_position
        print(f"POSISI diaomon: {diamond_position}")

        # Cari diamond terdekat dari bot
        print(f"DIAMOND COUNT: {len(board.diamonds)}")
        for i in range(1, len(board.diamonds)):
            distance_to_diamond_i = self.distance(
                board.diamonds[i].position.x,
                board_bot.position.x,
                board.diamonds[i].position.y,
                board_bot.position.y,
            )
            distance_to_diamond = self.distance(
                diamond_position.x,
                board_bot.position.x,
                diamond_position.y,
                board_bot.position.y,
            )

            # Cegah error inventory penuh
            if board.diamonds[i].properties.points == 2:
                if board_bot.properties.diamonds == 4:
                    print("DIAMOND 2 TAPI UDAH 4")
                    continue
            # # Cegah error inventory penuh
            # if board.diamonds[i].properties.points == 2 and board_bot.properties.diamonds == 4:
            #     print("DIAMOND 2 TAPI UDAH 4")
            #     continue

            elif distance_to_diamond_i < distance_to_diamond:
                diamond_position = board.diamonds[i].position
                self.goal_position = diamond_position
                diamond_position_new = diamond_position
                print(f"POSISI diaomon NEW: {diamond_position_new} ")

        return self.goal_position

    def avoid_teleport(self, board_bot: GameObject, board: Board):
        # WORK DETECT, MASIH STUPID MOVE
        teleporter_position = []
        print(f"BOT Sendiri: {board_bot}")
        for teleport in self.get_teleporter(board):
            teleporter_position.append((teleport.position.x, teleport.position.y))
        print(f"TELEPORTER: {teleporter_position}")

        our_bot = (board_bot.position.x, board_bot.position.y)
        print(f"OUR BOT: {our_bot}")
        if (board_bot.position.x + 1, board_bot.position.y) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "KANAN ADA TELEPORTER" + Style.RESET_ALL)
            if board_bot.position.x == 0:
                if board_bot.position.y == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI ATAS, BERGERAK KE BAWAH"
                        + Style.RESET_ALL
                    )
                    return 0, 1
                elif board_bot.position.y == board.height - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI BAWAH, BERGERAK KE ATAS"
                        + Style.RESET_ALL
                    )
                    return 0, -1
                else:
                    print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE + "BERGERAK KE KIRI" + Style.RESET_ALL)
                return -1, 0

        if (board_bot.position.x - 1, board_bot.position.y) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "KIRI ADA TELEPORTER" + Style.RESET_ALL)
            if board_bot.position.x == board.width - 1:
                if board_bot.position.y == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN ATAS, BERGERAK KE BAWAH"
                        + Style.RESET_ALL
                    )
                    return 0, 1
                elif board_bot.position.y == board.height - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN BAWAH, BERGERAK KE ATAS"
                        + Style.RESET_ALL
                    )
                    return 0, -1
                else:
                    print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                return 1, 0

        if (board_bot.position.x, board_bot.position.y + 1) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "BAWAH ADA TELEPORTER" + Style.RESET_ALL)
            if board_bot.position.y == 0:
                if board_bot.position.x == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI ATAS, BERGERAK KE KANAN"
                        + Style.RESET_ALL
                    )
                    return 1, 0
                elif board_bot.position.x == board.width - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN ATAS, BERGERAK KE KIRI"
                        + Style.RESET_ALL
                    )
                    return -1, 0
                else:
                    print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE + "BERGERAK KE ATAS" + Style.RESET_ALL)
                return 0, -1

        if (board_bot.position.x, board_bot.position.y - 1) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "ATAS ADA TELEPORTER" + Style.RESET_ALL)
            if board_bot.position.y == board.height - 1:
                if board_bot.position.x == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI BAWAH, BERGERAK KE KANAN"
                        + Style.RESET_ALL
                    )
                    return 1, 0
                elif board_bot.position.x == board.width - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN BAWAH, BERGERAK KE KIRI"
                        + Style.RESET_ALL
                    )
                    return -1, 0
                else:
                    print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                return 0, 1
        return None

    def defense_from_enemy(self, board: Board, board_bot: GameObject):
        bot_enemy_position = []
        print(f"BOT Sendiri: {board_bot}")
        print(f"ENEMY COUNT: {len(board.bots)}")
        for bots in board.bots:
            if bots.id != board_bot.id:
                bot_enemy_position.append((bots.position.x, bots.position.y))
        print(f"BOT ENEMY: {bot_enemy_position}")

        our_bot = (board_bot.position.x, board_bot.position.y)
        print(f"OUR BOT: {our_bot}")
        if (board_bot.position.x + 1, board_bot.position.y) in bot_enemy_position:
            # if board.height
            print(Fore.RED + Style.BRIGHT + "KANAN ADA MUSUH" + Style.RESET_ALL)
            # lakukan gerakan yang valid (tidak menabrak batas height dan widht matrix)
            if board_bot.position.x == 0:
                if board_bot.position.y == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI ATAS, BERGERAK KE BAWAH"
                        + Style.RESET_ALL
                    )
                    return 0, 1
                elif board_bot.position.y == board.height - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI BAWAH, BERGERAK KE ATAS"
                        + Style.RESET_ALL
                    )
                    return 0, -1
                else:
                    print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE + "BERGERAK KE KIRI" + Style.RESET_ALL)
                return -1, 0

        if (board_bot.position.x - 1, board_bot.position.y) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "KIRI ADA MUSUH" + Style.RESET_ALL)
            if board_bot.position.x == board.width - 1:
                if board_bot.position.y == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN ATAS, BERGERAK KE BAWAH"
                        + Style.RESET_ALL
                    )
                    return 0, 1
                elif board_bot.position.y == board.height - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN BAWAH, BERGERAK KE ATAS"
                        + Style.RESET_ALL
                    )
                    return 0, -1
                else:
                    print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                    return 0, 1
            else:
                print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                return 1, 0

        if (board_bot.position.x, board_bot.position.y + 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "BAWAH ADA MUSUH" + Style.RESET_ALL)
            if board_bot.position.y == 0:
                if board_bot.position.x == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI ATAS, BERGERAK KE KANAN"
                        + Style.RESET_ALL
                    )
                    return 1, 0
                elif board_bot.position.x == board.width - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN ATAS, BERGERAK KE KIRI"
                        + Style.RESET_ALL
                    )
                    return -1, 0
                else:
                    print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE + "BERGERAK KE ATAS" + Style.RESET_ALL)
                return 0, -1

        if (board_bot.position.x, board_bot.position.y - 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "ATAS ADA MUSUH" + Style.RESET_ALL)
            if board_bot.position.y == board.height - 1:
                if board_bot.position.x == 0:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KIRI BAWAH, BERGERAK KE KANAN"
                        + Style.RESET_ALL
                    )
                    return 1, 0
                elif board_bot.position.x == board.width - 1:
                    print(
                        Fore.BLUE
                        + "SUDAH DI POJOK KANAN BAWAH, BERGERAK KE KIRI"
                        + Style.RESET_ALL
                    )
                    return -1, 0
                else:
                    print(Fore.BLUE + "BERGERAK KE KANAN" + Style.RESET_ALL)
                    return 1, 0
            else:
                print(Fore.BLUE + "BERGERAK KE BAWAH" + Style.RESET_ALL)
                return 0, 1
        return None

    def tackle_enemy(self, board_bot: GameObject, board: Board):
        bot_enemy_position = []
        print(f"BOT Sendiri: {board_bot}")
        print(f"ENEMY COUNT: {len(board.bots)}")
        for bots in board.bots:
            if bots.id != board_bot.id:
                bot_enemy_position.append((bots.position.x, bots.position.y))
        print(f"BOT ENEMY: {bot_enemy_position}")

        our_bot = (board_bot.position.x, board_bot.position.y)
        print(f"OUR BOT: {our_bot}")
        print((board_bot.position.x + 1, board_bot.position.y))
        if (board_bot.position.x + 1, board_bot.position.y) in bot_enemy_position:
            # lakukan gerakan yang menabrak lawan (tidak menabrak batas height dan widht matrix)
            print(Fore.RED + Style.BRIGHT + "KANAN ADA MUSUH" + Style.RESET_ALL)
            return 1, 0

        if (board_bot.position.x - 1, board_bot.position.y) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "KIRI ADA MUSUH" + Style.RESET_ALL)
            return -1, 0

        if (board_bot.position.x, board_bot.position.y + 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "BAWAH ADA MUSUH" + Style.RESET_ALL)
            return 0, 1

        if (board_bot.position.x, board_bot.position.y - 1) in bot_enemy_position:
            print(Fore.RED + Style.BRIGHT + "ATAS ADA MUSUH" + Style.RESET_ALL)
            return 0, -1
        return None

    def clamp(self, n, smallest, largest):
        return max(smallest, min(n, largest))

    def get_direction(self, current_x, current_y, dest_x, dest_y):
        delta_x = self.clamp(dest_x - current_x, -1, 1)
        delta_y = self.clamp(dest_y - current_y, -1, 1)
        if delta_y != 0:
            delta_x = 0
        return (delta_x, delta_y)

    def next_move(self, board_bot: GameObject, board: Board):
        # if self.avoid_teleport(board_bot, board):
        #     self.timer_to_base += 1
        #     return self.avoid_teleport(board_bot, board)

        # if self.tackle_enemy(board_bot, board):
        #     self.timer_to_base += 1
        #     return self.tackle_enemy(board_bot, board)

        # if self.defense_from_enemy(board, board_bot):
        #     self.timer_to_base += 1
        #     return self.defense_from_enemy(board, board_bot)

        props = board_bot.properties
        base = board_bot.properties.base

        if self.sequenceMove:
            self.timer_to_base += 1
            return self.sequenceMove.pop(0)

        # Monitor jarak bot ke base
        distance_to_base = self.distance(
            base.x, board_bot.position.x, base.y, board_bot.position.y
        )
        print(f"BASE DIST: {distance_to_base}")

        # Pulang ketika inventory penuh
        if props.diamonds == 5:
            self.goal_position = base  # Base(y=10, x=3)

        # Base timing management
        elif self.timer_to_base >= 46:
            print(Fore.RED + "waktu pulang" + Style.RESET_ALL)
            if distance_to_base > 5:
                print(Fore.CYAN + "TOO FAR, PULANG NOW" + Style.RESET_ALL)
                self.goal_position = base
            elif self.timer_to_base >= 53:
                print(Fore.CYAN + "timer hit, PULANG" + Style.RESET_ALL)
                self.goal_position = base
            # else:
            #     print("BELUM WAKTUNYA BALIK")
            #     self.goal_position = self.closest_diamond(board, board_bot)

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
                    else:
                        delta_y = delta_x * -1

        teleporter_position = []
        print(f"BOT Sendiri: {board_bot}")
        for teleport in self.get_teleporter(board):
            teleporter_position.append((teleport.position.x, teleport.position.y))
        print(f"TELEPORTER: {teleporter_position}")

        our_bot = (board_bot.position.x, board_bot.position.y)
        print(f"OUR BOT: {our_bot}")

        if (current_position.x + delta_x, current_position.y) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "SB.X TELEPORTER" + Style.RESET_ALL)
            # ukur jarak y dari current_position ke goal_position
            y_distance_to_goal = self.goal_position.y - current_position.y
            if y_distance_to_goal > 0:
                delta_x = 0
                delta_y = 1
            else:
                delta_x = 0
                delta_y = -1

        if (current_position.x, current_position.y + delta_y) in teleporter_position:
            print(Fore.RED + Style.BRIGHT + "SB.Y TELEPORTER" + Style.RESET_ALL)
            # ukur jarak x dari current_position ke goal_position
            if delta_y == 1:
                self.sequenceMove.append((1, 0))
                self.sequenceMove.append((0, 1))
                self.sequenceMove.append((0, 1))
                self.sequenceMove.append((-1, 0))
            else:
                self.sequenceMove.append((1, 0))
                self.sequenceMove.append((0, -1))
                self.sequenceMove.append((0, -1))
                self.sequenceMove.append((-1, 0))
        # else:
        #     # Roam around
        #     delta = self.directions[self.current_direction]
        #     delta_x = delta[0]
        #     delta_y = delta[1]
        #     if random.random() > 0.6:
        #         self.current_direction = (self.current_direction + 1) % len(
        #             self.directions
        #         )

        # print("POSISI diaomon: ")
        # print(board.diamonds[0].position.x)

        # print("ALL DIAMONDS: ")
        # print(board.diamonds)
        if self.sequenceMove:
            delta_x, delta_y = self.sequenceMove.pop(0)
        self.timer_to_base += 1
        print(f"timer: {self.timer_to_base}")
        return delta_x, delta_y
