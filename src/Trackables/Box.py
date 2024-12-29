import numpy as np
from typing_extensions import Self

class Box(object):
    """
    It's a box with corners upper left, upper right, down left, down right
    """
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        def are_points_collinear(p1, p2, p3):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            if (x2 - x1) == 0 or (x3 - x2) == 0:
                return (x1 == x2) and (x1 == x3)

            m1 = (y2 - y1) / (x2 - x1)
            m2 = (y3 - y2) / (x3 - x2)

            return m1 == m2

        p1 = (x1, y1)
        p2 = (x2, y2)
        p3 = (x3, y3)
        p4 = (x4, y4)

        if are_points_collinear(p1, p2, p3) or are_points_collinear(p2, p4, p3) or are_points_collinear(p1, p2, p4) or are_points_collinear(p1, p3, p4):
            raise ValueError("3 or 4 points are collinear")

        p_all = [p1, p2, p3, p4]
        p_upper = []
        for i in range(2):
            up = min(p_all, key=lambda p: p[1])
            p_upper.append(up)
            p_all.remove(up)

        p_down = p_all
        self.p = []
        p = min(p_upper, key=lambda p: p[0])
        self.p.append(p)
        p_upper.remove(p)
        self.p.append(p_upper[0])
        p = min(p_down,  key=lambda p: p[0])
        self.p.append(p)
        p_down.remove(p)
        self.p.append(p_down[0])

    @classmethod
    def from2Corners(cls, x1, y1, x2, y2):
        """
        Creates Box from upper right and down left corners
        :param x1: x of upper left corner
        :param y1: y of upper left corner
        :param x2: x of down right corner
        :param y2: y of down right corner

        :return:
        """
        out = cls(x1, y1, x2, y1, x1, y2, x2, y2)
        return out

    @classmethod
    def almostEquel(cls, box1: Self, box2: Self, tolerance: float) -> bool:
        """
        Check if two boxes match within a given tolerance.
        :param box1: Box
        :param box2: Box
        :param tolerance: float - allowed error margin as a fraction of the box size.
        :return: bool - True if the boxes match within the tolerance, False otherwise.
        """
        sy = [0, 0]
        sy[0] = box1.p[0][1] - box1.p[2][1]
        sy[1]= box1.p[1][1] - box1.p[3][1]

        sx = [0, 0]
        sx[0] = box1.p[0][0] - box1.p[1][0]
        sx[1]= box1.p[2][0] - box1.p[3][0]

        for i, (p1, p2) in enumerate(zip(box1.p, box2.p)):
            sy_ = sy[i%2]
            sx_ = sx[int(i>2)]
            error_margin_x = abs(sx_ * tolerance)
            error_margin_y = abs(sy_ * tolerance)
            if not ((p1[0] - error_margin_x <= p2[0] <= p1[0]+error_margin_x) and (p1[1] - error_margin_y <= p2[1] <= p1[1]+error_margin_y)):
                return False
        return True

    def __eq__(self, other):
        return self.p == other.p

    def __str__(self):
        return f"Box({', '.join(map(lambda p: str(p).replace('(','' ).replace(')', ''), self.p))})"

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        out = Box(*self.p)
        return out

    def middle(self) -> tuple[float, float]:
        """
        returns middle point of the box
        :return tuple[float, float]: (x, y) the middle
        """
        val = list(zip(*self.p))
        x = sum(val[0])//4
        y = sum(val[1])//4
        return x, y

    def inside(self, point: tuple[int, int]) -> bool:
        """
        Checks if given point is inside the box.
        :param point: tuple[int, int] point (x, y) to check if is inside the box
        :return bool: True if inside the box, false otherwise
        """

        def y_line_function(A, B):
            x1, y1 = A
            x2, y2 = B
            m = (y2 - y1) / (x2 - x1)

            b = y1 - m * x1

            return lambda x: m * x + b

        def x_line_function(A, B):
            return y_line_function((A[1], A[0]), (B[1], B[0]))

        a, b, c, d = self.p
        px, py = point
        AB = y_line_function(a,b)
        BD = x_line_function(b,d)
        DC = y_line_function(d,c)
        CA = x_line_function(c,a)
        return py>=AB(px) and py<=DC(px) and px>=CA(py) and px<=BD(py)


    def getMask(self, shape: tuple[int, int]) -> np.ndarray:
        def triangle_mask(X, Y, p1, p2, p3):

            def area(px, py, qx, qy, rx, ry):
                return abs((px - rx) * (qy - ry) - (qx - rx) * (py - ry))

            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3

            total_area = area(x1, y1, x2, y2, x3, y3)
            area1 = area(X, Y, x2, y2, x3, y3)
            area2 = area(x1, y1, X, Y, x3, y3)
            area3 = area(x1, y1, x2, y2, X, Y)

            return np.isclose(area1 + area2 + area3, total_area)


        def quadrilateral_mask(p1, p2, p3, p4, grid_shape):
            Y, X = np.ogrid[:grid_shape[0], :grid_shape[1]]

            # Create masks for the two triangles
            mask_triangle1 = triangle_mask(X, Y, p1, p2, p3)
            mask_triangle2 = triangle_mask(X, Y, p1, p3, p4)

            # Combine the masks
            return mask_triangle1 | mask_triangle2


        # Example Usage

        mask = quadrilateral_mask(*self.p, grid_shape=shape)

        return mask

