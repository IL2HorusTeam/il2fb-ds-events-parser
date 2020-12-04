import datetime
import unittest

from il2fb.ds.events.definitions.smokes import HumanAircraftToggledWingtipSmokesEvent

from il2fb.ds.events.parsing.smokes import HumanAircraftToggledWingtipSmokesLineParser


class HumanAircraftToggledWingtipSmokesLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanAircraftToggledWingtipSmokesLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line_toggle_on(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")
    self.assertEqual(evt.data.actor.aircraft, "P-39D2")
    self.assertTrue(evt.data.state)
    self.assertEqual(evt.data.pos.x, float("91600.414"))
    self.assertEqual(evt.data.pos.y, float("73098.805"))
    self.assertEqual(evt.data.pos.z, float("661.9586"))

  def test_parse_line_toggle_off(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertFalse(evt.data.state)

  def test_parse_line_no_z_coord(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertEqual(evt.data.pos.z, 0)

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User :P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = " :P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = ":P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanAircraftToggledWingtipSmokesEvent)
    self.assertEqual(evt.data.actor.callsign, "")
