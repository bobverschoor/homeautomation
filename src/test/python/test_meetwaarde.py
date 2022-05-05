import datetime
import unittest

from entiteiten.electra import Electra
from entiteiten.meetwaarde import Meetwaarde, convertlist2tags, convertstr2tags


class MeetwaardeTest(unittest.TestCase):
    def test_meetwaarde_notags(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags={})
        self.assertEqual("10.0 testeenheid", str(mw))

    def test_meetwaarde_withtags(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags=convertlist2tags(["tag1:   iets  ",
                                                                                   "tag2: iets anders "]))
        self.assertEqual("10.0 testeenheid, tags: tag1=iets tag2=iets anders", str(mw))

    def test_meetwaarde_withtagsastring(self):
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags=convertstr2tags("tag1: iets"))
        self.assertEqual("10.0 testeenheid, tags: tag1=iets", str(mw))

    def test_meetwaarde_withtimestamp(self):
        now = datetime.datetime.now()
        mw = Meetwaarde(eenheid="testeenheid", waarde=10.0, tags={}, timestamp=now)
        self.assertEqual("10.0 testeenheid", str(mw))
        self.assertEqual(now, mw.timestamp)

    def test_convert2tags(self):
        tags = ["zonderdubbelepunt"]
        self.assertRaises(ValueError, convertlist2tags, tags)
        tags = "zonderdubbelepunt"
        self.assertRaises(ValueError, convertlist2tags, tags)
        tags = [" goede Tagnaam : tag Value", " andere goede tagnaam  :  tag value"]
        self.assertEqual({"goede Tagnaam": "tag Value", "andere goede tagnaam": "tag value"}, convertlist2tags(tags))

    def test_electra(self):
        now = datetime.datetime.now()
        e = Electra(waarde=230.0, tarief=Electra.LAAGTARIEF, richting=Electra.VERBRUIKT, fase="l1", tags={},
                    timestamp=now)
        self.assertEqual("230.0 Wh, tags: tarief=laag richting=verbruikt, tarief: laag, richting: verbruikt, fase: l1",
                         str(e))
        with self.assertRaises(ValueError):
            e = Electra(waarde=230.0, tarief="Onbekend", richting=Electra.VERBRUIKT, fase="l1", tags={})
        with self.assertRaises(ValueError):
            e = Electra(waarde=230.0, tarief=Electra.LAAGTARIEF, richting="onbekend", fase="l1", tags={})
