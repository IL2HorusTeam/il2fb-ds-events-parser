import datetime
import unittest

from il2fb.ds.events.definitions.spawning import AIAircraftDespawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftDespawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedEvent

from il2fb.ds.events.parsing.spawning import HumanAircraftSpawnedLineParser
from il2fb.ds.events.parsing.spawning import AircraftDespawnedLineParser


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


class AircraftDespawnedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = AircraftDespawnedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F removed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftDespawnedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.actor.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.pos.x, float("145663.6"))
    self.assertEqual(evt.data.pos.y, float("62799.64"))
    self.assertEqual(evt.data.pos.z, float("83.96088"))

  def test_parse_line_human_aircraft_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftDespawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_human_aircraft_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftDespawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = " :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftDespawnedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

  def test_parse_line_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01200 removed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftDespawnedEvent)
    self.assertEqual(evt.data.actor.regiment_id, "r01")
    self.assertEqual(evt.data.actor.squadron_id, 2)
    self.assertEqual(evt.data.actor.flight_id, 0)
    self.assertEqual(evt.data.actor.flight_index, 0)

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 removed at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftDespawnedEvent)
    self.assertEqual(evt.data.pos.z, 0)
