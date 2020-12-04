import datetime
import unittest

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent

from il2fb.ds.events.parsing.recording import HumanToggledRecordingLineParser


class HumanToggledRecordingLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanToggledRecordingLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line_toggle_on(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser started NTRK record"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanToggledRecordingEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertTrue(evt.data.state)

  def test_parse_line_toggle_off(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser stopped NTRK record"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanToggledRecordingEvent)
    self.assertFalse(evt.data.state)

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User stopped NTRK record"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanToggledRecordingEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "  stopped NTRK record"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanToggledRecordingEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = " stopped NTRK record"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanToggledRecordingEvent)
    self.assertEqual(evt.data.actor.callsign, "")
