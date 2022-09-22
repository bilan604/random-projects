import sys
from BattleShip import game

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments given.')
    else:
        game_of_battle_ship = game.Game(sys.argv[1])
        random_seed = sys.argv[2] #the seed
        game_of_battle_ship.play()
        
