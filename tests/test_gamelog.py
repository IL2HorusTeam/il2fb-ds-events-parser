import unittest

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldEvent

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent

from il2fb.ds.events.definitions.lights import HumanToggledLandingLightsEvent

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent
from il2fb.ds.events.definitions.smokes import HumanToggledWingtipSmokesEvent

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.gamelog import GamelogLineParser
from il2fb.ds.events.parsing.mission import MissionLoadedLineParser


class GamelogLineParserTestCase(unittest.TestCase):

  def test_default_subparsers(self):
    parser = GamelogLineParser()

    items = [
      (MissionLoadedEvent,                   "[Aug 3, 2020 3:46:08 PM] Mission: net/dogfight/1596469535.mis is Playing"),
      (MissionStartedEvent,                  "[3:46:08 PM] Mission BEGIN"),
      (MissionEndedEvent,                    "[3:46:16 PM] Mission END"),

      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM] TheUser has connected"),
      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM]  The User  has connected"),
      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM]   has connected"),
      (HumanConnectionEstablishedLightEvent, "[3:50:25 PM]  has connected"),

      (HumanConnectionLostLightEvent,        "[3:50:25 PM] TheUser has disconnected"),
      (HumanConnectionLostLightEvent,        "[3:50:25 PM]  The User  has disconnected"),
      (HumanConnectionLostLightEvent,        "[3:50:25 PM]   has disconnected"),
      (HumanConnectionLostLightEvent,        "[3:50:25 PM]  has disconnected"),

      (HumanReturnedToBriefingEvent,         "[3:50:25 PM] TheUser entered refly menu"),
      (HumanReturnedToBriefingEvent,         "[3:50:25 PM]  The User  entered refly menu"),
      (HumanReturnedToBriefingEvent,         "[3:50:25 PM]   entered refly menu"),
      (HumanReturnedToBriefingEvent,         "[3:50:25 PM]  entered refly menu"),

      (HumanSelectedAirfieldEvent,           "[6:55:50 PM] TheUser selected army Red at 134055.0 136158.0"),
      (HumanSelectedAirfieldEvent,           "[6:55:50 PM] TheUser selected army Red at 134055.0 136158.0 0.0"),
      (HumanSelectedAirfieldEvent,           "[6:55:50 PM]  The User  selected army Red at 134055.0 136158.0 0.0"),
      (HumanSelectedAirfieldEvent,           "[6:55:50 PM]   selected army Red at 134055.0 136158.0 0.0"),
      (HumanSelectedAirfieldEvent,           "[6:55:50 PM]  selected army Red at 134055.0 136158.0 0.0"),

      (HumanToggledRecordingEvent,           "[3:46:16 PM] TheUser started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM] TheUser stopped NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]  The User  started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]  The User  stopped NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]   started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]   stopped NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]  started NTRK record"),
      (HumanToggledRecordingEvent,           "[3:46:16 PM]  stopped NTRK record"),

      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM]  The User :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM]  :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"),
      (HumanToggledLandingLightsEvent,       "[3:50:25 PM] :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"),

      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM]  The User :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM]  :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"),
      (HumanToggledWingtipSmokesEvent,       "[3:50:25 PM] :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"),
    ]

    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

  def test_custom_subparsers(self):
    parser = GamelogLineParser([
      MissionLoadedLineParser(),
    ])

    line = "[Aug 3, 2020 3:46:08 PM] Mission: net/dogfight/1596469535.mis is Playing"
    evt  = parser.parse_line(line)
    self.assertIsInstance(evt, MissionLoadedEvent)

    line = "[3:50:25 PM] TheUser has disconnected"
    evt  = parser.parse_line(line)
    self.assertIsNone(evt)
