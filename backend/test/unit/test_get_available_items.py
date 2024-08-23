
import pytest
from src.util.dao import DAO
from src.controllers.controller import Controller

class MockDAO(DAO):
    def __init__(self, items):
        self.items = items

    def find(self):
        return self.items

class TestController(pytest.TestCase):
    def setUp(self):
        self.controller = None

    @pytest.mark.unit
    def test_get_available_items(self):
        # Test case 1: Items list is empty
        self.controller = Controller(MockDAO([]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=0), {})

        # Test case 2: All items have quantities above minimum_quantity
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 5}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=3), {"Rice": 10, "Beans": 5})

        # Test case 3: All items have quantities below minimum_quantity
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 2},
            {"name": "Beans", "quantity": 1}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=3), {})

        # Test case 4: Items with quantities equal to minimum_quantity
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 5},
            {"name": "Beans", "quantity": 5}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=5), {})

        # Test case 5: Items with quantities both above and below minimum_quantity
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 2}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=5), {"Rice": 10})

        # Test case 6: minimum_quantity = -1 (return all items)
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 5},
            {"name": "Pasta", "quantity": 0}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=-1), {"Rice": 10, "Beans": 5, "Pasta": 0})

        # Test case 7: Negative Value: minimum_quantity = -2
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 5},
            {"name": "Pasta", "quantity": 0}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=-2), {"Rice": 10, "Beans": 5, "Pasta": 0})

        # Test case 8: minimum_quantity = 0
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 5},
            {"name": "Pasta", "quantity": 0}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=0), {"Rice": 10, "Beans": 5})

        # Test case 9: High Positive Value: minimum_quantity = 10000
        self.controller = Controller(MockDAO([
            {"name": "Rice", "quantity": 10},
            {"name": "Beans", "quantity": 5},
            {"name": "Pasta", "quantity": 0}
        ]))
        self.assertEqual(self.controller.get_available_items(minimum_quantity=10000), {})

    @pytest.mark.unit
    def test_get_all_raises_exception(self):
        class ExceptionDAO(DAO):
            def find(self):
                raise Exception("Database error")

        self.controller = Controller(ExceptionDAO())
        
        self.assertIsNone(self.controller.get_available_items())
