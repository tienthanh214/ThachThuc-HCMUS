class State: 
    def __init__(self, x1, y1, x2, y2, p1, s1, p2, s2, alive1, alive2, moveleft, map):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.p1 = p1
        self.s1 = bool(s1)
        self.p2 = p2
        self.s2 = bool(s2)
        self.alive1 = bool(alive1)
        self.alive2 = bool(alive2)
        self.moveleft = moveleft
        self.map = map
    def __str__(self):
        return f"""{self.x1} {self.y1} {self.x2} {self.y2}\
            {self.p1} {'has shield' if self.s1 else 'not shield'}\
            {self.p2} {'has shield' if self.s2 else 'not shield'}\
            {'dead' if not self.alive1 else 'alive'}\
            {'dead' if not self.alive2 else 'alive'}"""
    def to_dict(self):
        return {
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'point1': self.p1,
            'shield1': self.s1,
            'point2': self.p2,
            'shield2': self.s2,
            'alive1': self.alive1,
            'alive2': self.alive2,
            'moveleft': self.moveleft,
            # 'map': self.map,
            'map_humanreadable': [','.join(row) for row in self.map]
        }
    @staticmethod
    def from_players(p1, p2, moveleft, map):
        return State(p1.x, p1.y, p2.x, p2.y, p1.point, p1.shield, p2.point, p2.shield, p1.alive, p2.alive, moveleft, map)