from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals


class BotTaski4(BaseLogic):
    """
    BOT GERIDI By
    ! TEKAN TOMBOL MERAH kalo jarak ke tombol merah <= 4
    ? defense: ga ada
    attack: ga ada
    """

    def __init__(self):
        self.timer_to_base = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def diamond_button_position(self, board: Board):
        for temp in board.game_objects:
            if temp.type == "DiamondButtonGameObject":
                return temp.position
        return None

    def check_diamond(self, board: Board) -> bool:
        # check if the diamond in goal position is still there
        for diamond in board.diamonds:
            if position_equals(diamond.position, self.goal_position):
                return True
        return False

    def distance(self, pos1: Position, pos2: Position):
        # hitung jarak antara dua titik
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        # Analyze new state
        if props.diamonds >= 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        elif self.distance(current_position, self.diamond_button_position(board)) <= 4:
            diamond_button = self.diamond_button_position(board)
            self.goal_position = diamond_button
        else:
            while self.goal_position is None:
                # Just roam around
                diamond = self.dia(board)
                if diamond:
                    self.goal_position = diamond

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

        self.timer_to_base += 1
        return delta_x, delta_y
