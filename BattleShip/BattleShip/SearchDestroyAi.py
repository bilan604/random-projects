from typing import Dict
from . import board
from . import ship


class SearchDestroyAi(object):

    def __init__(self, ships: Dict[str, ship.Ship], board_info: board.Board):
        self.type_name = "SearchDestroy"
        self.ships = ships
        self.row = board_info.number_rows
        self.col = board_info.number_cols
        self.destroy = False
        self.placement_locations = []
        self.firing_list = []
        self.firing_list_progress = 0
        for i in range(self.row):
            for j in range(self.col):
                self.placement_locations.append([int(i), int(j)])
        self.firing_locations = []
        for i in range(self.row):
            for j in range(self.col):
                self.firing_locations.append([int(i), int(j)])



