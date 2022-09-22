from typing import Dict
from . import ship


class GameConfig(object):
    def __init__(self, game_config_file: str) -> None:
        super().__init__()
        self._num_rows = -1
        self._num_cols = -1
        self.available_ships: Dict[str, ship.Ship] = {}
        with open(game_config_file) as config_file:   #here
            board_dims = config_file.readline()
            self._num_rows, self._num_cols = map(int, board_dims.split())
            for ship_info in config_file:
                ship_name, ship_len = ship_info.split()
                ship_len = int(ship_len)
                self.available_ships[ship_name[0]] = ship.Ship(ship_name, ship_len)

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols

    def is_legal_ship_symbol(self, ship_name: str) -> bool:
        return ship_name in self.available_ships
