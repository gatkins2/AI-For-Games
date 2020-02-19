from math import sqrt


# Class to represent a 2D Vector
class Vector:

    # Constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Return a vector of (0, 0)
    @staticmethod
    def zero():
        return Vector(0, 0)

    # Tuple form
    def tuple(self):
        return (self.x, self.y)

    # Print
    def __str__(self):
        return "Vector(" + str(self.x) + ", " + str(self.y) + ")"

    # Operator overloads
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    # Return the dot product of two vectors
    def dot(self, other):
        xProd = self.x * other.x
        yProd = self.y * other.y
        return xProd + yProd

    # Return the vector scaled by a float value
    def scale(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector(x, y)

    # Return the magnitude of the vector
    def length(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    # Return a normalized version of the vector
    def normalize(self):
        if self.length() != 0:
            x = self.x / self.length()
            y = self.y / self.length()
        else:
            x = 0
            y = 0
        return Vector(x, y)