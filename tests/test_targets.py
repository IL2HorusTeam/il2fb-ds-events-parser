import datetime
import unittest

from il2fb.commons.targets import TARGET_STATES

from il2fb.ds.events.definitions.targets import TargetStateChangedEvent

from il2fb.ds.events.parsing.targets import TargetStateChangedLineParser


class TargetStateChangedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = TargetStateChangedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 8, 3, 15, 46, 8)
    line = "Target 3 Complete"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, TargetStateChangedEvent)

    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.index, 3)
    self.assertEqual(evt.data.state, TARGET_STATES.COMPLETE)
