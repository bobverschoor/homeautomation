import unittest

from entiteiten.weer import Weer


class TestWeer(unittest.TestCase):
    def test_weer(self):
        weer = Weer()
        weer._error = ""
        weer.temperatuur = "bla"
        self.assertTrue(weer.error)
        weer._error = ""
        weer.temperatuur = -51
        self.assertTrue(weer.error)
        weer._error = ""
        weer.temperatuur = 51
        self.assertTrue(weer.error)
        weer._error = ""
        weer.windrichting = "NA"
        self.assertTrue(weer.error)
        weer._error = ""
        weer.windrichting = "NNW"
        self.assertFalse(weer.error)
        self.assertEqual(337.5, weer.windrichting)
        weer.windrichting = "noord"
        self.assertFalse(weer.error)
        self.assertEqual(0.0, weer.windrichting)
