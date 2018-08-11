class Entity:
    """Base class for game units/monsters/player

    blocking -- is walking on this blocked?
    """
    def __init__(self, x, y, char, color, game):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.game = game
        self.map = game.map
        self.blocking = True

    def move(self, dx, dy):
        if not self.map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def teleport_to(self, x, y):
        if self.map.in_bounds(x, y):
            self.x = x
            self.y = y
