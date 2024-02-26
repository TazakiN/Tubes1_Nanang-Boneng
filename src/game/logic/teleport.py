import random
from ..util import get_direction
from time import sleep

from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position

class TeleporterShake(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        sleep(0.5);
        # Analyze new state
            # Move towards first diamond on board
        self.goal_position = board.game_objects[0].get("position");
        print(self.goal_position)
        if self.goal_position:
            # Calculate move according to goal position
            current_position = board_bot["position"]
            delta_x, delta_y = get_direction(current_position["x"], current_position["y"],
                    self.goal_position["x"], self.goal_position["y"])
            if delta_x == 0 and delta_y == 0: 
                return 1,1; 
            return delta_x, delta_y

        return 0, 0