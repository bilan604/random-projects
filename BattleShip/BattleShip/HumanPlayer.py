from typing import Dict
from . import board
from . import ship


class HumanPlayer(object):

    def __init__(self, ships: Dict[str, ship.Ship], board_info: board.Board):
        self.ships = ships
        self.board = board_info
        self.type_name = "Human"
        self.possible_locations = []
        for i in range(self.board.num_rows):
            for j in range(self.board.num_cols):
                self.possible_locations.append([int(i), int(j)])
