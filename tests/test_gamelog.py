import unittest

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent

from il2fb.ds.events.parsing.gamelog import GamelogLineParser

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionLostLightLineParser


class GamelogLineParserTestCase(unittest.TestCase):

  def test_default_subparsers(self):
    parser = GamelogLineParser()
    items = [
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM] TheUser has connected",
      ),
      (
        HumanConnectionLostLightEvent,
        "[3:50:25 PM] TheUser has disconnected",
      ),
    ]
    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

  def test_custom_subparsers(self):
    parser = GamelogLineParser([
      HumanConnectionEstablishedLightLineParser(),
    ])

    items = [
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM] TheUser has connected",
      ),
    ]
    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

    ignored_items = [
      "[3:50:25 PM] TheUser has disconnected",
    ]
    for line in ignored_items:
      result = parser.parse_line(line)
      self.assertIsNone(result, msg=f"line={line!r}")
