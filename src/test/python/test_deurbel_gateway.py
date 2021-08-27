import time
import unittest

from sensor.deurbel_gateway import DeurbelGateway, DeurbelGatewayException


class MockDeurbelKnop:
    def __init__(self):
        self.knopwaarde = False

    def is_ingedrukt(self):
        return self.knopwaarde


class MockDeurbelGong:
    def __init__(self):
        self.gong_rang = False
        self.gong_duration = -1

    def ring(self, duration):
        now = time.time()
        self.gong_rang = True
        time.sleep(duration)
        self.gong_duration = round(time.time() - now, 1)


class DeurbelGatewaytest(unittest.TestCase):

    def test_gateway_init(self):
        self.assertRaises(DeurbelGatewayException, DeurbelGateway, {})
        deurbel = DeurbelGateway({DeurbelGateway.CONFIG_DEURBEL: {}})
        self.assertEqual(deurbel._gongduration, 1)
        deurbel = DeurbelGateway({DeurbelGateway.CONFIG_DEURBEL: {DeurbelGateway.CONFIG_GONGDURATION: 2}})
        self.assertEqual(deurbel._gongduration, 2)

    def test_parallel_aanroep_gong(self):
        gong_duration = 0.9
        deurbel = DeurbelGateway({DeurbelGateway.CONFIG_DEURBEL: {DeurbelGateway.CONFIG_GONGDURATION: gong_duration}})
        deurbel._knop = MockDeurbelKnop()
        deurbel._gong = MockDeurbelGong()
        deurbel._knop.knopwaarde = False
        self.assertFalse(deurbel.someone_at_the_deur())
        self.assertFalse(deurbel._gong.gong_rang)
        deurbel._knop.knopwaarde = True
        now = time.time()
        self.assertTrue(deurbel.someone_at_the_deur())
        knop_duration = round(time.time() - now, 1)
        self.assertEqual(0, knop_duration)
        self.assertTrue(deurbel._gong.gong_rang)
        self.assertEqual(-1, deurbel._gong.gong_duration)
        while deurbel._gong.gong_duration == -1:
            pass
        self.assertEqual(gong_duration, deurbel._gong.gong_duration)


if __name__ == '__main__':
    unittest.main()
