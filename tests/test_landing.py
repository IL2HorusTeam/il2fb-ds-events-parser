import datetime
import unittest

from il2fb.ds.events.definitions.landing import AIAircraftLandedEvent
from il2fb.ds.events.definitions.landing import HumanAircraftLandedEvent

from il2fb.ds.events.parsing.landing import ActorLandedLineParser


class ActorLandedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = ActorLandedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F landed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftLandedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.actor.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.pos.x, float("145663.6"))
    self.assertEqual(evt.data.pos.y, float("62799.64"))
    self.assertEqual(evt.data.pos.z, float("83.96088"))

  def test_parse_line_human_aircraft_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :TB-7_M40F landed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftLandedEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_human_aircraft_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :TB-7_M40F landed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftLandedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = ":TB-7_M40F landed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftLandedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

  def test_parse_line_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01200 landed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftLandedEvent)
    self.assertEqual(evt.data.actor.id, "r0120")
    self.assertEqual(evt.data.actor.flight_index, 0)

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 landed at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftLandedEvent)
    self.assertEqual(evt.data.pos.z, 0)
