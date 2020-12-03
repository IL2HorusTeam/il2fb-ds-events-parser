import datetime
import unittest

from il2fb.commons.belligerents import BELLIGERENTS

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldEvent

from il2fb.ds.events.parsing.briefing import HumanReturnedToBriefingLineParser
from il2fb.ds.events.parsing.briefing import HumanSelectedAirfieldLineParser


class HumanReturnedToBriefingLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanReturnedToBriefingLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.time(15, 46, 8)
    line = "TheUser entered refly menu"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanReturnedToBriefingEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")


class HumanSelectedAirfieldLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanSelectedAirfieldLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse(self):
    timestamp = datetime.time(15, 46, 8)
    line = "TheUser selected army Red at 134055.0 136158.0 0.0"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanSelectedAirfieldEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.belligerent, BELLIGERENTS.RED)
    self.assertEqual(evt.data.pos.x, 134055.0)
    self.assertEqual(evt.data.pos.y, 136158.0)
    self.assertEqual(evt.data.pos.z, 0)

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.time(15, 46, 8)
    line = "TheUser selected army Red at 134055.0 136158.0"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanSelectedAirfieldEvent)
    self.assertEqual(evt.data.pos.z, 0)
