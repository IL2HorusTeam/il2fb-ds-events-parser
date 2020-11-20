import unittest

from il2fb.ds.events.definitions.cheating import CheatingDetectedEvent

from il2fb.ds.events.parsing.cheating import CheatingLineParser


class CheatingLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = CheatingLineParser()

  def test_parse_line_no_match(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    line = "socket channel '203' Cheater was detected! Reason=8: 'Cheat-Engine'"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, CheatingDetectedEvent)
    self.assertEqual(evt.data.channel_no, 203)
    self.assertEqual(evt.data.cheat_code, 8)
    self.assertEqual(evt.data.cheat_details, "Cheat-Engine")
