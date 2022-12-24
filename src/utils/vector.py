from math import sqrt


class Vector:
    def __init__(self, x: float, y: float):
        if isinstance(x, float) and isinstance(y, float):
            self.__x = x
            self.__y = y
        raise ValueError

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def is_perpendicular(self, v):
        if isinstance(v, Vector):
            return self * v == 0
        raise ValueError

    def __abs__(self):
        return self.length()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(other.x + self.x, other.y + self.y)
        raise ValueError

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        raise ValueError

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, Vector):
            return other.x * self.x + other.y * self.y
        raise TypeError

    def __str__(self):
        return f'v({self.x}; {self.y})'
