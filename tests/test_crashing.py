import datetime
import unittest

from il2fb.ds.events.definitions.crashing import AIAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import HumanAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitMemberCrashedEvent
from il2fb.ds.events.definitions.crashing import StationaryUnitCrashedEvent

from il2fb.ds.events.parsing.crashing import ActorCrashedLineParser


class ActorCrashedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = ActorCrashedLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftCrashedEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.actor.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.pos.x, float("145663.6"))
    self.assertEqual(evt.data.pos.y, float("62799.64"))
    self.assertEqual(evt.data.pos.z, float("83.96088"))

  def test_parse_line_human_aircraft_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftCrashedEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_human_aircraft_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftCrashedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = ":TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftCrashedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

  def test_parse_line_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01200 crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftCrashedEvent)
    self.assertEqual(evt.data.actor.id, "r0120")
    self.assertEqual(evt.data.actor.flight_index, 0)

  def test_parse_line_stationary_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "0_Static crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, StationaryUnitCrashedEvent)
    self.assertEqual(evt.data.actor.id, '0_Static')

  def test_parse_line_moving_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "0_Chief crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, MovingUnitCrashedEvent)
    self.assertEqual(evt.data.actor.id, '0_Chief')

  def test_parse_line_moving_unit_member(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "0_Chief1 crashed at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, MovingUnitMemberCrashedEvent)
    self.assertEqual(evt.data.actor.id, '0_Chief')
    self.assertEqual(evt.data.actor.member_index, 1)

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 crashed at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftCrashedEvent)
    self.assertEqual(evt.data.pos.z, 0)
