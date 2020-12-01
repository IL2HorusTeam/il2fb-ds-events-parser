import unittest

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent

from il2fb.ds.events.definitions.lights import HumanToggledLandingLightsEvent

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.gamelog import GamelogLineParser
from il2fb.ds.events.parsing.mission import MissionLoadedLineParser


class GamelogLineParserTestCase(unittest.TestCase):

  def test_default_subparsers(self):
    parser = GamelogLineParser()

    items = [
      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM] TheUser has connected"),
      (HumanConnectionLostLightEvent,        "[3:50:25 PM] TheUser has disconnected"),
      (MissionLoadedEvent,                   "[Aug 3, 2020 3:46:08 PM] Mission: net/dogfight/1596469535.mis is Playing"),
      (MissionStartedEvent,                  "[3:46:08 PM] Mission BEGIN"),
      (MissionEndedEvent,                    "[3:46:16 PM] Mission END"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM] TheUser started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM] TheUser stopped NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]   started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]   stopped NTRK record"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805"),
    ]

    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

  def test_custom_subparsers(self):
    parser = GamelogLineParser([
      HumanConnectionEstablishedLightLineParser(),
      MissionLoadedLineParser(),
    ])

    items = [
      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM] TheUser has connected"),
      (MissionLoadedEvent,                   "[Aug 3, 2020 3:46:08 PM] Mission: net/dogfight/1596469535.mis is Playing"),
    ]
    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

    ignored_items = [
      "[3:50:25 PM] TheUser has disconnected",
      "[3:46:08 PM] Mission BEGIN",
      "[3:46:16 PM] Mission END",
      "[3:46:16 PM] TheUser started NTRK record",
      "[3:46:16 PM] TheUser stopped NTRK record",
      "[3:46:16 PM] started NTRK record",
      "[3:46:16 PM] stopped NTRK record",
    ]
    for line in ignored_items:
      result = parser.parse_line(line)
      self.assertIsNone(result, msg=f"line={line!r}")
