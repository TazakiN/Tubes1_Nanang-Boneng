from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals


class TaskiLogic3(BaseLogic):
    """
    BOT GERIDI By Radius Bot ke Diamond terdekat
    Bakal ngelakuin pencarian diamond dengan radius 1, 2, 3, dst
    kalo ketemu diamond, bakal ngikutin diamond tersebut
    kalo diamondnya ilang, bakal cari diamond lagi
    kalo diamondnya udah 4, bakal balik ke base

    defense: ga ada
    attack: ga ada
    !! udah ada tambahan fungsi untuk ngecek teleporter
    ! blom ada fungsi untuk menghindari teleporter (masih dikembangin)
    """

    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def get_teleporter(self, board: Board):
        return [t for t in board.game_objects if t.type == "TeleportGameObject"]

    def closest_diamond_button_position(self, board: Board):
        for temp in board.game_objects:
            if temp.type == "DiamondButtonGameObject":
                return temp.position
        return None

    def is_near_teleporter(
        self, board_bot: GameObject, board: Board
    ) -> Optional[Position]:
        current_position = board_bot.position
        # cek jarak antara bot dengan teleporter
        for teleporter in self.get_teleporter(board):
            if (
                abs(current_position.x - teleporter.position.x) <= 2
                and abs(current_position.y - teleporter.position.y) <= 2
            ):
                return teleporter.position
        return None

    def is_near_diamond_button(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        # cek jarak antara bot dengan diamond button
        diamond_button = self.closest_diamond_button_position(board)
        if (
            abs(current_position.x - diamond_button.position.x) <= 2
            and abs(current_position.y - diamond_button.position.y) <= 2
        ):
            return diamond_button.position
        return None

    def distance(self, x2, x1, y2, y1):
        # hitung jarak antara dua titik
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def closest_diamond(self, board: Board, board_bot: GameObject):
        diamond_position = board.diamonds[0].position
        self.goal_position = diamond_position
        print("POSISI diaomon: ")
        print(diamond_position)

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
            if (
                board.diamonds[i].properties.points == 2
                and board_bot.properties.diamonds == 4
            ):
                print("DIAMOND 2 TAPI UDAH 4")
                continue

            elif distance_to_diamond_i < distance_to_diamond:
                diamond_position = board.diamonds[i].position
                self.goal_position = diamond_position
                diamond_position_new = diamond_position
                print("POSISI diaomon NEW: ")
                print(diamond_position_new)

        return self.goal_position

    def check_diamond(self, board: Board) -> bool:
        # check if the diamond in goal position is still there
        for diamond in board.diamonds:
            if position_equals(diamond.position, self.goal_position):
                return True
        return False

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        # Analyze new state
        if props.diamonds >= 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            print("RECALL RECALL")
        else:
            while self.goal_position is None:
                # Just roam around
                diamond = self.closest_diamond(board, board_bot)
                if diamond:
                    self.goal_position = diamond
                else:
                    # increment search radius
                    rad += 1

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

            if (delta_x == 0 and delta_y == 0) or not self.check_diamond(board):
                if not self.check_diamond(board):
                    print("DIAMOND HILANG")
                self.goal_position = None

        # periksa apakah ada teleporter di langkah yang dituju
        for teleporter in self.get_teleporter(board):
            print(teleporter.position, end=" ")
            print(current_position)
            if position_equals(
                Position(current_position.x + delta_x, current_position.y),
                teleporter.position,
            ):
                print("TELEPORTER DI SB.X")
                # ukur jarak y dari current_position ke goal_position
                y_distance_to_goal = self.goal_position.y - current_position.y
                if y_distance_to_goal > 0:
                    delta_x = 0
                    delta_y = 1
                else:
                    delta_x = 0
                    delta_y = -1

            if position_equals(
                Position(current_position.x, current_position.y + delta_y),
                teleporter.position,
            ):
                print("TELEPORTER DI SB.Y")
                # ukur jarak x dari current_position ke goal_position
                x_distance_to_goal = self.goal_position.x - current_position.x
                if x_distance_to_goal > 0:
                    delta_x = 1
                    delta_y = 0
                else:
                    delta_x = -1
                    delta_y = 0
        return delta_x, delta_y
