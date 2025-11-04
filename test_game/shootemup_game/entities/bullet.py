class Bullet:
    def __init__(self, x: int, y: int, speed: int = 2):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = speed