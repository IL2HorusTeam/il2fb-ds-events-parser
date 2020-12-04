import datetime
import unittest

from pathlib import Path

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent

from il2fb.ds.events.parsing.mission import MissionLoadedLineParser
from il2fb.ds.events.parsing.mission import MissionStartedLineParser
from il2fb.ds.events.parsing.mission import MissionEndedLineParser


class MissionLoadedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = MissionLoadedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 8, 3, 15, 46, 8)
    line = "Mission: net/dogfight/1596469535.mis is Playing"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, MissionLoadedEvent)

    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.file_path, Path("net/dogfight/1596469535.mis"))


class MissionStartedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = MissionStartedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "Mission BEGIN"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, MissionStartedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)


class MissionEndedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = MissionEndedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "Mission END"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, MissionEndedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
