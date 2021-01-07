import math
from decimal import Decimal, getcontext
from typing import Iterable


class Vector:
    """class Vector(iterable).
    Iterable must be a sequence, a container that supports iteration or an iterator object.

    The Vector class uses decimal floating point arithmetic, provided by Python's
    module 'decimal'.
    The decimal floating point accuracy can be defined by the user; default value is 30 significant digits.
    """

    def __init__(self, coordinates: Iterable, tolerance=Decimal('1e-15')):
        try:
            if not coordinates:
                raise ValueError
            else:
                self.coordinates = tuple(Decimal(x) for x in coordinates)
                self.dimension = len(self.coordinates)
                self.tolerance = tolerance
                # Set the number of significant digits for the decimal calculations
                getcontext().prec = 30
        except ValueError:
            raise ValueError('Coordinates must be non-empty')
        except TypeError:
            raise TypeError('Coordinates must be an iterable')

    def __str__(self):
        """Return a string representation of the vector."""
        return 'Vector: {}'.format(self.coordinates)

    def __getitem__(self, i):
        """Make the vector indexable."""
        return self.coordinates[i]

    def __iter__(self):
        """Make the vector iterable."""
        return self.coordinates.__iter__()

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        """Scalar multiplication or inner product (dot product).

        This method detects the attempted type of multiplication and returns the appropriate result.
        """
        if isinstance(other, (int, float, Decimal, str)):
            return Vector(x * Decimal(other) for x in self.coordinates)
        elif isinstance(other, Vector):
            return self.dot(other)
        else:
            return NotImplemented

    def add(self, other):
        return Vector(x + y for x, y in zip(self.coordinates, other.coordinates))

    def subtract(self, other):
        return Vector(x - y for x, y in zip(self.coordinates, other.coordinates))

    def dot(self, other):
        return sum(x * y for x, y in zip(self.coordinates, other.coordinates))

    def magnitude(self):
        """Return the magnitude of this vector.

        Uses the Decimal.sqrt() method provided by the decimal module to preserve the decimal accuracy.
        """
        return sum(x ** 2 for x in self.coordinates).sqrt()

    def normalized(self):
        """Return the normalization of this vector."""
        m = self.magnitude()
        if m.is_zero():
            raise ZeroDivisionError('Cannot normalize the zero vector')
        return Vector(x / m for x in self.coordinates)

    def is_zero(self):
        """Check if this vector is the zero vector within a specified tolerance."""
        return self.magnitude() < self.tolerance

    def angle_with(self, other, in_degrees=False):
        """Returns the angle θ between this vector and the 'other' vector.

        If in_degrees is True the angle is returned in degrees.
        """
        try:
            angle = math.acos(self.normalized() * other.normalized())
            if in_degrees:
                return math.degrees(angle)
            else:
                return angle
        except ZeroDivisionError:
            raise ArithmeticError('Cannot compute an angle with the zero vector')

    def is_orthogonal_to(self, other):
        """Check if this vector is orthogonal to the other vector within a specified tolerance."""
        return abs(self * other) < self.tolerance

    def is_parallel_to(self, other):
        """Check if this vector is parallel to the 'other' within a specified tolerance."""
        if self.is_zero() or other.is_zero():
            return True
        elif abs(abs(self * other) - self.magnitude() * other.magnitude()) < self.tolerance:
            return True
        else:
            return False

    def orthogonal_to(self, other):
        """Returns the orthogonal component of this vector to the 'other' vector."""
        try:
            return self - self.parallel_to(other)
        except ArithmeticError:
            raise ArithmeticError('No unique orthogonal component to zero vector')

    def parallel_to(self, other):
        """Return the parallel component (projection) of this vector to the 'other' vector."""
        try:
            norm_other = other.normalized()
            return (self * norm_other) * norm_other
        except ZeroDivisionError:
            raise ArithmeticError('No unique parallel component to zero vector')

    def cross(self, other):
        """Return the cross product of this vector to the 'other' vector.

        Note: Cross product is defined only in three dimensions.
        """
        if not (self.dimension == other.dimension == 3):
            raise Exception('Cross product is only defined in three dimensions')
        x = self.coordinates[1] * other.coordinates[2] - self.coordinates[2] * other.coordinates[1]
        y = -(self.coordinates[0] * other.coordinates[2] - self.coordinates[2] * other.coordinates[0])
        z = self.coordinates[0] * other.coordinates[1] - self.coordinates[1] * other.coordinates[0]
        return Vector([x, y, z])


def test_vector():
    a = Vector([1., 2., 0])
    b = Vector(['6.984', '-5.975', '4.778'])
    c = Vector(['0.0000000000000000001', '0.0000000000000001', 0])
    d = Vector([1, '2.00000000000000000000001', 0])
    f = Vector([0, 0])
    v = Vector(['8.462', '7.893', '-8.187'])
    z = Vector([0, 0, 0])

    print("\n***** TESTING VECTOR: *****\n")
    print("a = {}".format(a))
    print("||a|| = {}".format(a.magnitude()))

    print("b = {}".format(b))
    print("||b|| = {}".format(b.magnitude()))

    print("c = {}".format(c))
    print("||c|| = {}".format(c.magnitude()))

    print("d = {}".format(d))
    print("||d|| = {}".format(d.magnitude()))

    print("f = {}".format(f))
    print("||f|| = {}".format(f.magnitude()))

    print()
    print("a normalized: {}".format(a.normalized()))
    print("b normalized: {}".format(b.normalized()))
    # print("f normalized: {}".format(f.normalized()))

    print()
    print("a + b - c = {}".format(a + b - c))
    print("a + b - c = {}".format(a.add(b).subtract(c)))
    print("a * b = {}".format(a * b))
    print("a * b = {}".format(a.dot(b)))
    print("'0.1' * a * b = {}".format('.1' * a * b))

    print()
    print("Angle between a and c in radians: {}".format(a.angle_with(c)))
    print("Angle between a and c in degrees: {}".format(a.angle_with(c, in_degrees=True)))

    print()
    print("c is zero within a tolerance of 1e-15: {}".format(c.is_zero()))

    print()
    print("a is orthogonal to c within a tolerance of 1e-15: {}".format(a.is_orthogonal_to(c)))

    print()
    print("a is parallel to c within a tolerance of 1e-15: {}".format(a.is_parallel_to(c)))

    print()
    print("a is parallel to d within a tolerance of 1e-15: {}".format(a.is_parallel_to(d)))

    print()
    print("Parallel of v onto b: {}".format(v.parallel_to(b)))
    print("Orthogonal of v onto b: {}".format(v.orthogonal_to(b)))

    print()
    print("Cross product v x b = {}".format(v.cross(b)))


if __name__ == "__main__":
    test_vector()
