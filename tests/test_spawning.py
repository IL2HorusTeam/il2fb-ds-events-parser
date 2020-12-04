import datetime
import unittest

from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedEvent

from il2fb.ds.events.parsing.spawning import HumanAircraftSpawnedLineParser


class HumanAircraftSpawnedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanAircraftSpawnedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:Pe-2series84 loaded weapons '2fab500' fuel 50%"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftSpawnedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.actor.aircraft, "Pe-2series84")
    self.assertEqual(evt.data.weapons, "2fab500")
    self.assertEqual(evt.data.fuel, 50)

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :Pe-2series84 loaded weapons '2fab500' fuel 50%"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftSpawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :Pe-2series84 loaded weapons '2fab500' fuel 50%"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftSpawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = " :Pe-2series84 loaded weapons '2fab500' fuel 50%"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftSpawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "")
