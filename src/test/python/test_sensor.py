import unittest

from entiteiten.sensor import Sensor, SensorException, Schakelaar, TemperatuurSensor, LichtSensor


class TestSensor(unittest.TestCase):
    def test_sensor(self):
        sensor = Sensor(1)
        with self.assertRaises(SensorException):
            sensor.batterijpercentage = -1
        with self.assertRaises(SensorException):
            sensor.batterijpercentage = "sdf"
        with self.assertRaises(SensorException):
            sensor.bereikbaar = "geen booolean"
        sensor.bereikbaar = 'False'
        self.assertFalse(sensor.bereikbaar)
        with self.assertRaises(SensorException):
            sensor.tijdstip_meting = "gisteren"

    def test_schakelaar(self):
        schakelaar = Schakelaar(2)
        schakelaar.knop_id = Schakelaar.DIMMER_OMLAAG
        self.assertEqual(Schakelaar.DIMMER_OMLAAG, schakelaar.knop_id)
        self.assertEqual(Schakelaar.DIMMER_OMLAAG_TXT, schakelaar.knop_waarde)
        with self.assertRaises(SensorException):
            schakelaar.knop_id = -9

    def test_temperatuur_sensor(self):
        tempsensor = TemperatuurSensor(3)
        with self.assertRaises(SensorException):
            tempsensor.temperature = "geen waarde"
        tempsensor.temperature = 3.7
        self.assertEqual(3, tempsensor.temperature)

    def test_lichtsensor(self):
        lichtsensor = LichtSensor(4)
        with self.assertRaises(SensorException):
            lichtsensor.lichtniveau = "laag"
        with self.assertRaises(SensorException):
            lichtsensor.lichtniveau = -10
        lichtsensor.lichtniveau = 1000
        self.assertEqual(3, lichtsensor.lichtniveau_lux)
