from typing import Dict
from . import board
from . import ship


class CheatingAi(object):

    def __init__(self, ships: Dict[str, ship.Ship], board_info: board.Board, opponent):
        self.type_name = "CheatingAi"
        self.ships = ships
        self.row = board_info.number_rows #int
        self.col = board_info.number_cols #int

        self.placement_locations = []
        for i in range(self.row):
            for j in range(self.col):
                self.placement_locations.append([int(i), int(j)])
        self.firing_locations = []