from decimal import Decimal
from Vector import Vector


class Line:
    """Line([normal_vector[, constant_term, tolerance]]).

    Construct a 2-d Line object from:
    - normal_vector, a two-dimensional Vector object (the line's normal vector)
    - constant_term, a number (int, long, float), a Decimal number or a string
    - tolerance, a Decimal tolerance for equality comparisons. Defaults to 1e-15
    """

    NO_NONZERO_ELTS_FOUND_MSG = 'No non-zero elements found'

    def __init__(self, normal_vector=None, constant_term=None, tolerance=Decimal('1e-15')):
        self.tolerance = tolerance
        self.dimension = 2
        if not normal_vector:
            normal_vector = Vector([0 for _ in range(self.dimension)], tolerance=self.tolerance)
        self.normal_vector = normal_vector
        if not constant_term:
            constant_term = Decimal(0)
        self.constant_term = Decimal(constant_term)
        self.set_basepoint()

    def set_basepoint(self):
        """Calculate a base point for the line."""
        try:
            basepoint_coords = ['0' for _ in range(self.dimension)]
            initial_index = self.first_nonzero_index()
            initial_coefficient = self.normal_vector[initial_index]
            basepoint_coords[initial_index] = self.constant_term / initial_coefficient
            self.base_point = Vector(basepoint_coords)
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.base_point = None
            else:
                raise

    def first_nonzero_index(self):
        for position, item in enumerate(self.normal_vector):
            if not abs(item) < self.tolerance:
                return position
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def __str__(self):
        """Return a string representation of this line."""
        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)
            output = ''
            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'
            if not is_initial_term:
                output += ' '
            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))
            return output

        num_decimal_places = 3
        n = self.normal_vector
        try:
            initial_index = self.first_nonzero_index()
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)
        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise
        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)
        return output

    def is_parallel_to(self, other):
        """Check if this line is parallel to the 'other' line within the specified tolerance."""
        return self.normal_vector.is_parallel_to(other.normal_vector)

    def __eq__(self, other):
        """Check if this line is equal to the 'other' line within the specified tolerance."""
        # To be equal the two lines must first be parallel:
        if self.is_parallel_to(other):
            # First check the edge cases of zero normal vectors
            if self.normal_vector.is_zero():
                if not other.normal_vector.is_zero():
                    return False
                else:
                    diff = self.constant_term - other.constant_term
                    return abs(diff) < self.tolerance
            elif other.normal_vector.is_zero():
                return False
            # Both normal vectors are non-zero. Check the connecting vector of the two lines
            connecting_vector = self.base_point - other.base_point
            if connecting_vector.is_zero() or connecting_vector.is_orthogonal_to(self.normal_vector):
                return True
        return False

    def intersection(self, other):
        """Return the intersection of this line with the 'other' line.

        - If lines are parallel the method returns None.
        - If lines are equal the method returns self."""
        if self == other:
            return self
        elif self.is_parallel_to(other):
            return None
        else:
            a, b, c = self.normal_vector[0], self.normal_vector[1], self.constant_term
            d, e, f = other.normal_vector[0], other.normal_vector[1], other.constant_term
            x = (c * e - b * f) / (a * e - b * d)
            y = (a * f - d * c) / (a * e - b * d)
            return x, y


def test_line():
    l1 = Line(normal_vector=Vector(['10.115', '7.09']), constant_term='0.1')
    l2 = Line(normal_vector=Vector(['10.115', '7.09']), constant_term='3.025')
    l3 = Line(normal_vector=Vector(['7.204', '3.182']), constant_term='8.68')
    l4 = Line(normal_vector=Vector(['8.172', '4.114']), constant_term='9.883')
    l5 = Line(normal_vector=Vector(['1.182', '5.562']), constant_term='6.744')
    l6 = Line(normal_vector=Vector(['1.773', '8.343']), constant_term='9.525')

    print("\n***** TESTING LINE: *****\n")
    print("Line 1: {}".format(l1))
    print("Line 2: {}".format(l2))
    print("Line 3: {}".format(l3))
    print("Line 4: {}".format(l4))
    print("Line 5: {}".format(l5))
    print("Line 6: {}".format(l6))
    print()
    print("Line 1 is parallel to line 2: {}".format(l1.is_parallel_to(l2)))
    print()
    print("Line 1 is equal to line 2: {}".format(l1 == l2))
    print()
    print("Line 1 intersection with line 2: {}".format(l1.intersection(l2)))
    print()
    print("Line 3 intersection with line 4: {}".format(l3.intersection(l4)))
    print()
    print("Line 5 intersection with line 6: {}".format(l5.intersection(l6)))
    print()
    print("Line 6 intersection with line 6: {}".format(l6.intersection(l6)))


if __name__ == "__main__":
    test_line()
