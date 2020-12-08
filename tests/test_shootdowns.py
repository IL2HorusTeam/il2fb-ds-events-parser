import datetime
import unittest

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownSelfEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownSelfEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBridgeEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBuildingEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitMemberEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByObjectEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByStationaryUnitEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByTreeEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByParatrooperEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBridgeEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBuildingEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitMemberEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByObjectEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByStationaryUnitEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByTreeEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByParatrooperEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent

from il2fb.ds.events.parsing.shootdowns import ActorShotdownLineParser


class ActorShotdownLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = ActorShotdownLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_ai_aircraft_shotdown(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by  at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.pos.x, float("145663.6"))
    self.assertEqual(evt.data.pos.y, float("62799.64"))
    self.assertEqual(evt.data.pos.z, float("83.96088"))

  def test_ai_aircraft_shotdown_self(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "r01001 shot down by landscape at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownSelfEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)

    line = "r01001 shot down by NONAME at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownSelfEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)

  def test_ai_aircraft_shotdown_by_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by g01002 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)

  def test_ai_aircraft_shotdown_by_bridge(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by  Bridge159 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByBridgeEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "Bridge159")

  def test_ai_aircraft_shotdown_by_building(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 194_bld at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByBuildingEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "194_bld")

  def test_ai_aircraft_shotdown_by_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by TheUser:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.callsign, "TheUser")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")

  def test_ai_aircraft_shotdown_by_human_aircraft_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by  The User :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "TheUser")

  def test_ai_aircraft_shotdown_by_human_aircraft_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "r01001 shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "")

    line = "r01001 shot down by :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "")

  def test_ai_aircraft_shotdown_by_moving_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 0_Chief at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByMovingUnitEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "0_Chief")

  def test_ai_aircraft_shotdown_by_moving_unit_member(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 0_Chief0 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByMovingUnitMemberEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "0_Chief")
    self.assertEqual(evt.data.attacker.member_index, 0)

  def test_ai_aircraft_shotdown_by_object(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByObjectEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "3do/Buildings/Airdrome/BarrelBlock1/mono.sim")

  def test_ai_aircraft_shotdown_by_stationary_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 0_Static at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByStationaryUnitEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "0_Static")

  def test_ai_aircraft_shotdown_by_tree(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByTreeEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)

  def test_ai_aircraft_shotdown_by_paratrooper(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by _para_1 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByParatrooperEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)

  def test_human_aircraft_shotdown(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownEvent)
    self.assertEqual(evt.data.target.callsign, "TheUser")

  def test_human_aircraft_shotdown_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownEvent)
    self.assertEqual(evt.data.target.callsign, "")

    line = ":TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownEvent)
    self.assertEqual(evt.data.target.callsign, "")

  def test_human_aircraft_shotdown_self(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "TheUser:TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownSelfEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")

    line = "TheUser:TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownSelfEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_by_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)

  def test_human_aircraft_shotdown_by_bridge(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByBridgeEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "Bridge159")

  def test_human_aircraft_shotdown_by_building(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByBuildingEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "194_bld")

  def test_human_aircraft_shotdown_by_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.callsign, "TheUser2")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_by_human_aircraft_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "TheUser2")

  def test_human_aircraft_shotdown_by_human_aircraft_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "TheUser:TB-7_M40F shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "")

    line = "TheUser:TB-7_M40F shot down by :TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftEvent)
    self.assertEqual(evt.data.attacker.callsign, "")

  def test_human_aircraft_shotdown_by_moving_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByMovingUnitEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "0_Chief")

  def test_human_aircraft_shotdown_by_moving_unit_member(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByMovingUnitMemberEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "0_Chief")
    self.assertEqual(evt.data.attacker.member_index, 0)

  def test_human_aircraft_shotdown_by_object(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByObjectEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "3do/Buildings/Airdrome/BarrelBlock1/mono.sim")

  def test_human_aircraft_shotdown_by_stationary_unit(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 0_Static at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByStationaryUnitEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "0_Static")

  def test_human_aircraft_shotdown_by_tree(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByTreeEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_by_paratrooper(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByParatrooperEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")

  def test_ai_aircraft_shotdown_by_ai_aircraft_and_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by g01002 and g01003 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByAIAircraftAndAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)
    self.assertEqual(evt.data.assistant.id, "g0100")
    self.assertEqual(evt.data.assistant.flight_index, 3)

  def test_ai_aircraft_shotdown_by_ai_aircraft_and_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by g01002 and TheUser:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByAIAircraftAndHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)
    self.assertEqual(evt.data.assistant.callsign, "TheUser")
    self.assertEqual(evt.data.assistant.aircraft, "TB-7_M40F")

  def test_ai_aircraft_shotdown_by_human_aircraft_and_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by TheUser:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftAndAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.callsign, "TheUser")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.assistant.id, "g0100")
    self.assertEqual(evt.data.assistant.flight_index, 2)

  def test_ai_aircraft_shotdown_by_human_aircraft_and_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by TheUser:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.id, "r0100")
    self.assertEqual(evt.data.target.flight_index, 1)
    self.assertEqual(evt.data.attacker.callsign, "TheUser")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.assistant.callsign, "TheUser2")
    self.assertEqual(evt.data.assistant.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_by_ai_aircraft_and_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by g01002 and g01003 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByAIAircraftAndAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)
    self.assertEqual(evt.data.assistant.id, "g0100")
    self.assertEqual(evt.data.assistant.flight_index, 3)

  def test_human_aircraft_shotdown_by_ai_aircraft_and_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by g01002 and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.id, "g0100")
    self.assertEqual(evt.data.attacker.flight_index, 2)
    self.assertEqual(evt.data.assistant.callsign, "TheUser2")
    self.assertEqual(evt.data.assistant.aircraft, "TB-7_M40F")

  def test_human_aircraft_shotdown_by_human_aircraft_and_ai_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.callsign, "TheUser2")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.assistant.id, "g0100")
    self.assertEqual(evt.data.assistant.flight_index, 2)

  def test_human_aircraft_shotdown_by_human_aircraft_and_human_aircraft(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and TheUser3:TB-7_M40F at 145663.6 62799.64 83.96088"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.attacker.callsign, "TheUser2")
    self.assertEqual(evt.data.attacker.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.assistant.callsign, "TheUser3")
    self.assertEqual(evt.data.assistant.aircraft, "TB-7_M40F")

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by  at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, AIAircraftShotdownEvent)
    self.assertEqual(evt.data.pos.z, 0)

  def test_parse_line_unknown_target(self):
    timestamp = None
    line = "xxx shot down by  at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)
    self.assertIsNone(evt)

  def test_parse_line_unknown_attaker(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by xxx at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)
    self.assertIsInstance(evt, AIAircraftShotdownEvent)

  def test_parse_line_unknown_assistant(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by g01001 and xxx at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)
    self.assertIsInstance(evt, AIAircraftShotdownByAIAircraftEvent)

  def test_parse_line_unknown_attaker_and_known_assistant(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by xxx and g01001 at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)
    self.assertIsInstance(evt, AIAircraftShotdownByAIAircraftEvent)

  def test_parse_line_unknown_attaker_and_unknown_assistant(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "r01001 shot down by xxx and zzz at 145663.6 62799.64"
    evt = self.parser.parse_line(timestamp, line)
    self.assertIsInstance(evt, AIAircraftShotdownEvent)
