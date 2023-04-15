from _global import logger

class Player:
    def __init__(self, id, num_rows, num_cols):
        self.id = id
        self.x = 0
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.y = 0
        self.point = 0
        self.alive = True
        self.shield = False

    def set_pos(self, _x, _y):
        self.x = _x
        self.y = _y

    def go(self, _x, _y):
        if self.alive:
            if abs(self.x - _x) + abs(self.y - _y) == 1 and 1 <= _x <= self.num_rows and 1 <= _y <= self.num_cols:
                logger.append(f'[{self.id}] Move from ({self.x}, {self.y}) to ({_x}, {_y})')
                self.x = _x
                self.y = _y
            else:
                logger.append(f'[{self.id}] Invalid move from ({self.x}, {self.y}) to ({_x}, {_y})')

    def earn_point(self, v):
        if self.alive:
            logger.append(f'[{self.id}] Get {v} coins.')
            self.point += v

    def equip_shield(self):
        if self.alive:
            logger.append(f'[{self.id}] Equip shield.')
            self.shield |= 1
    
    def encounter_trap(self):
        if self.alive:
            logger.append(f'[{self.id}] Encounter trap.')
            if not self.shield:
                self.die()

    def die(self):
        if self.alive:
            logger.append(f'[{self.id}] dies.')
            self.alive = False
