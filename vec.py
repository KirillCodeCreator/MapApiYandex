class Vec:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __mul__(self, other):
        if type(other) != Vec:
            return Vec(self.x * other, self.y * other)
        return Vec(self.x * other.x, self.y * other.y)

    @property
    def xy(self):
        return self.x, self.y

    def to_ym(self):
        return f'{round(self.x, 6)},{round(self.y, 6)}'
