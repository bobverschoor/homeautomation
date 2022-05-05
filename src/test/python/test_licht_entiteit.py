import unittest

from entiteiten.licht import LichtException, Licht


class LichtTest(unittest.TestCase):
    def test_licht(self):
        with self.assertRaises(LichtException):
            l = Licht("sdf")
        l = Licht(1)
        with self.assertRaises(LichtException):
            l.bereikbaar = "geen boolean"
