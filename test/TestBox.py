import unittest

from src.Trackables.Box import Box

class TestBox(unittest.TestCase):
    def test_constructor(self):
        box = Box(0, 0, 2, 0, 0, 2, 2, 2)
        self.assertEqual(
            (0, 0, 2, 0, 0, 2, 2, 2),
            (box.p[0][0], box.p[0][1], box.p[1][0], box.p[1][1], box.p[2][0], box.p[2][1], box.p[3][0], box.p[3][1]))
        box_combinations = []

        points = [(0, 0), (2, 0), (0, 2), (2, 2)]
        describtions = ["p1", "p2", "p3", "p4"]

        for i in range(4):
            for j in range(4):
                if i <= j:
                    continue
                p = points.copy()
                p[i], p[j] = p[j], p[i]

                new_box = Box(p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1])
                description = f"failed for: {' '.join(describtions)}"
                box_combinations.append((new_box, description))

        for idx, (box, desc) in enumerate(box_combinations):
            self.assertEqual(
                (0, 0, 2, 0, 0, 2, 2, 2),
                (box.p[0][0], box.p[0][1], box.p[1][0], box.p[1][1], box.p[2][0], box.p[2][1], box.p[3][0], box.p[3][1]),
                msg=desc)


    def test_from2Corners(self):
        box = Box.from2Corners(0, 0, 2, 2)

        self.assertEqual(
        (box.p[0][0], box.p[0][1], box.p[1][0], box.p[1][1], box.p[2][0], box.p[2][1], box.p[3][0], box.p[3][1]),
        (0, 0, 2, 0, 0, 2, 2, 2))

    def test_almostEqual(self):
        box1 = Box.from2Corners(0, 0, 20, 20)
        box2 = Box.from2Corners(0, 0, 21, 21)
        box3 = Box.from2Corners(0, 0, 30, 30)

        self.assertTrue(Box.almostEquel(box1, box2, tolerance=0.1))
        self.assertFalse(Box.almostEquel(box1, box3, tolerance=0.1))

    def test_equality(self):
        box1 = Box.from2Corners(0, 0, 2, 2)
        box2 = Box.from2Corners(0, 0, 2, 2)
        box3 = Box.from2Corners(1, 1, 3, 3)

        self.assertEqual(box1, box2)
        self.assertNotEqual(box1, box3)

    def test_middle(self):
        box = Box(0, 0, 2, 0, 0, 2, 2, 2)
        self.assertEqual((1,1), box.middle())

    def test_inside(self):
        # Symetryczny prostokąt
        box = Box.from2Corners(0, 0, 4, 4)

        # Punkty wewnątrz
        inside_points = [(2, 2), (1, 1), (3, 3)]
        for point in inside_points:
            with self.subTest(point=point):
                self.assertTrue(box.inside(point))

        # Punkty na krawędzi
        edge_points = [(0, 0), (4, 0), (0, 4), (4, 4), (2, 0), (0, 2), (4, 2), (2, 4)]
        for point in edge_points:
            with self.subTest(point=point):
                self.assertTrue(box.inside(point), f"failed for {point}")

        # Punkty na zewnątrz
        outside_points = [(5, 5), (-1, -1), (5, 0), (0, 5), (4.1, 4.1), (-0.1, -0.1)]
        for point in outside_points:
            with self.subTest(point=point):
                self.assertFalse(box.inside(point))

        # Niesymetryczny czworokąt
        nonsym_box = Box(0, 0, 3, 1, 1, 4, 4, 3)

        # Punkty wewnątrz
        nonsym_inside_points = [(1, 1), (1, 2), (1, 2), (2, 2)]
        for point in nonsym_inside_points:
            with self.subTest(point=point):
                self.assertTrue(nonsym_box.inside(point), f"failed for {point}")

        # Punkty na zewnątrz
        nonsym_outside_points = [(5, 5), (-1, -1), (4.5, 3.5), (2, 5), (-0.5, -0.5)]
        for point in nonsym_outside_points:
            with self.subTest(point=point):
                self.assertFalse(nonsym_box.inside(point))

        # Niesymetryczny czworokąt
        nonsym_box = Box(0, 0, 30, 10, 10, 40, 33, 30)

        # Punkty wewnątrz
        nonsym_inside_points = [(1, 1), (7, 7), (30, 13), (30, 11), (32, 29)]
        for point in nonsym_inside_points:
            with self.subTest(point=point):
                self.assertTrue(nonsym_box.inside(point), f"failed for {point}")

        # Punkty na zewnątrz
        nonsym_outside_points = [(100, 100), (1, 0), (30,9), (32, 32), (11, 40)]
        for point in nonsym_outside_points:
            with self.subTest(point=point):
                self.assertFalse(nonsym_box.inside(point), f"failed for {point}. Should be outside is considered inside")

if __name__ == "__main__":
    unittest.main()
