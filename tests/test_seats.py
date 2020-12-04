import datetime
import unittest

from il2fb.ds.events.definitions.seats import HumanOccupiedCrewMemberSeatEvent

from il2fb.ds.events.parsing.seats import HumanOccupiedCrewMemberSeatLineParser


class HumanOccupiedCrewMemberSeatLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanOccupiedCrewMemberSeatLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F(2) seat occupied by TheUser at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanOccupiedCrewMemberSeatEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.target.callsign, "TheUser")
    self.assertEqual(evt.data.target.aircraft, "TB-7_M40F")
    self.assertEqual(evt.data.target.crew_index, 2)
    self.assertEqual(evt.data.pos.x, float("91600.414"))
    self.assertEqual(evt.data.pos.y, float("73098.805"))
    self.assertEqual(evt.data.pos.z, float("661.9586"))

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:TB-7_M40F(2) seat occupied by TheUser at 91600.414 73098.805"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanOccupiedCrewMemberSeatEvent)
    self.assertEqual(evt.data.pos.z, 0)

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :TB-7_M40F(2) seat occupied by  The User  at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanOccupiedCrewMemberSeatEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.target.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :TB-7_M40F(2) seat occupied by   at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanOccupiedCrewMemberSeatEvent)
    self.assertEqual(evt.data.actor.callsign, "")
    self.assertEqual(evt.data.target.callsign, "")

    line = ":TB-7_M40F(2) seat occupied by  at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanOccupiedCrewMemberSeatEvent)
    self.assertEqual(evt.data.actor.callsign, "")
    self.assertEqual(evt.data.target.callsign, "")
