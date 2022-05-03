import datetime
import unittest

from entiteiten.meetwaarde import Meetwaarde, convert2tags


class MeetwaardeTest(unittest.TestCase):
    def test_meetwaarde_notags(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags={})
        self.assertEqual("10.0 testeenheid", str(mw))

    def test_meetwaarde_withtags(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags=convert2tags(["tag1: iets  ", "tag2: iets anders"]))
        self.assertEqual("10.0 testeenheid, tags: tag1=iets tag2=iets anders", str(mw))

    def test_meetwaarde_withtagsastring(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags=convert2tags("tag1: iets  "))
        self.assertEqual("10.0 testeenheid, tags: tag1=iets", str(mw))

    def test_meetwaarde_withtimestamp(self):
        now = datetime.datetime.now()
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags={}, timestamp=now)
        self.assertEqual("10.0 testeenheid", str(mw))
        self.assertEqual(now, mw.timestamp)


if __name__ == '__main__':
    unittest.main()
