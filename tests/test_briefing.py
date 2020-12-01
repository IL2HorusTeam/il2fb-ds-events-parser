import datetime
import unittest

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent

from il2fb.ds.events.parsing.briefing import HumanReturnedToBriefingLineParser


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
