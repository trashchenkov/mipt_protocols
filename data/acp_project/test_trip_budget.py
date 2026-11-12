import unittest

from trip_budget import total_cost


class TripBudgetTests(unittest.TestCase):
    def test_two_products_with_quantities(self):
        self.assertEqual(total_cost([(120, 2), (80, 3)]), 480)

    def test_single_product(self):
        self.assertEqual(total_cost([(90, 1)]), 90)

    def test_empty_cart(self):
        self.assertEqual(total_cost([]), 0)

    def test_zero_quantity(self):
        self.assertEqual(total_cost([(120, 0)]), 0)


if __name__ == "__main__":
    unittest.main()
