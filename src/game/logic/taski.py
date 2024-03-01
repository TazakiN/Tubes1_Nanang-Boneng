from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals


class BotTaski(BaseLogic):
    """
    BOT GERIDI By Radius Bot ke Diamond terdekat
    Bakal ngelakuin pencarian diamond dengan radius 1, 2, 3, dst
    kalo ketemu diamond, bakal ngikutin diamond tersebut
    kalo diamondnya ilang, bakal cari diamond lagi
    kalo diamondnya udah 4, bakal balik ke base
    defense: ga ada
    attack: ga ada
    """

    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def search_diamond(
        self, board_bot: GameObject, board: Board, search_radius: int
    ) -> Optional[Position]:
        current_position = board_bot.position
        for i in range(-(search_radius), search_radius + 1):
            for j in range(-(search_radius), search_radius + 1):
                if i == 0 and j == 0:
                    continue
                temp_diamond = Position(current_position.x + i, current_position.y + j)
                for diamond in board.diamonds:
                    if diamond.position == temp_diamond:
                        print("DIAMOND FOUND at ", temp_diamond.x, temp_diamond.y)
                        return temp_diamond
        return None

    def search_diamond_greedy(
        self, board_bot: GameObject, board: Board, search_radius: int
    ) -> Optional[Position]:
        current_position = board_bot.position
        best_diamond_position = None
        best_distance = float("inf")

        for i in range(-(search_radius), search_radius + 1):
            for j in range(-(search_radius), search_radius + 1):
                temp_diamond = Position(current_position.x + i, current_position.y + j)
                for diamond in board.diamonds:
                    if diamond.position == temp_diamond:
                        distance = abs(temp_diamond.x - current_position.x) + abs(
                            temp_diamond.y - current_position.y
                        )
                        if distance < best_distance:
                            best_distance = distance
                            best_diamond_position = temp_diamond

        return best_diamond_position

    def check_diamond(self, board: Board) -> bool:
        # check if the diamond in goal position is still there
        for diamond in board.diamonds:
            if position_equals(diamond.position, self.goal_position):
                return True
        return False

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        # Analyze new state
        if props.diamonds >= 4 and self.goal_position is None:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
            print("RECALL RECALL")
        else:
            rad = 1
            while self.goal_position is None:
                # Just roam around
                diamond = self.search_diamond_greedy(board_bot, board, rad)
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

            if delta_x == 0 and delta_y == 0:
                if not self.check_diamond(board):
                    print("DIAMOND HILANG")
                self.goal_position = None

        return delta_x, delta_y
