import pyxel

class JumpItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_show = False
        self.is_getted = False

    def get_item(self, player):
        if not self.is_getted:
            player.max_jumps += 1
            self.is_show = False
            self.is_getted = True
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 24, 8, 8, 0)
    
    def update(self, player):
        if (abs(self.x - player.x) < 24 and self.y == player.y and
            not self.is_getted and not self.is_show):
            self.is_show = True

class SpeedItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_show = False
        self.is_getted = False

    def get_item(self, player):
        if not self.is_getted:
            player.max_speed = min(player.max_speed + 0.5, 6)
            player.accelerration += 0.05
            self.is_show = False
            self.is_getted = True
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 8, 8, 8, 0)
    
    def update(self, player):
        if (8 < self.x - player.x < 32 and abs(self.y - player.y) < 24 and
            not self.is_getted and not self.is_show):
            self.is_show = True
    