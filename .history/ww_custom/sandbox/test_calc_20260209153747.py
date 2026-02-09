import unittest
from calc import add, subtract, multiply, divide, power

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(-1, 1), -2)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 5), -10)

    def test_divide(self):
        self.assertEqual(divide(20, 5), 4)
        self.assertEqual(divide(-15, 3), -5)
        with self.assertRaises(ValueError):
            divide(10, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(3, 2), 9)

if __name__ == '__main__':
    unittest.main()
