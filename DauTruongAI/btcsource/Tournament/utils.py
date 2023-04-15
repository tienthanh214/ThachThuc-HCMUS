class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __repr__(self):
        return f'({self.x}, {self.y})'
