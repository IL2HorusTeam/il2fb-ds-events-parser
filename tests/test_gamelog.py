import unittest

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldEvent

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent

from il2fb.ds.events.definitions.crashing import AIAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import HumanAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitMemberCrashedEvent
from il2fb.ds.events.definitions.crashing import StationaryUnitCrashedEvent

from il2fb.ds.events.definitions.landing import HumanAircraftLandedEvent
from il2fb.ds.events.definitions.landing import AIAircraftLandedEvent

from il2fb.ds.events.definitions.lights import HumanAircraftToggledLandingLightsEvent

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent
from il2fb.ds.events.definitions.mission import MissionWonEvent

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent
from il2fb.ds.events.definitions.seats import HumanOccupiedCrewMemberSeatEvent
from il2fb.ds.events.definitions.smokes import HumanAircraftToggledWingtipSmokesEvent

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

from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedEvent

from il2fb.ds.events.definitions.spawning import AIAircraftDespawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftDespawnedEvent

from il2fb.ds.events.definitions.takeoff import HumanAircraftTookOffEvent

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.gamelog import GamelogLineParser
from il2fb.ds.events.parsing.mission import MissionLoadedLineParser


class GamelogLineParserTestCase(unittest.TestCase):

  def test_default_subparsers(self):
    parser = GamelogLineParser()

    items = [
      (
        MissionLoadedEvent,
        "[Aug 3, 2020 3:46:08 PM] Mission: net/dogfight/1596469535.mis is Playing",
      ),
      (
        MissionStartedEvent,
        "[3:46:08 PM] Mission BEGIN",
      ),
      (
        MissionEndedEvent,
        "[3:46:16 PM] Mission END",
      ),
      (
        MissionWonEvent,
        "[Aug 3, 2020 3:46:08 PM] Mission: RED WON",
      ),
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM] TheUser has connected",
      ),
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM]  The User  has connected",
      ),
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM]   has connected",
      ),
      (
        HumanConnectionEstablishedLightEvent,
        "[3:50:25 PM]  has connected",
      ),
      (
        HumanConnectionLostLightEvent,
        "[3:50:25 PM] TheUser has disconnected",
      ),
      (
        HumanConnectionLostLightEvent,
        "[3:50:25 PM]  The User  has disconnected",
      ),
      (
        HumanConnectionLostLightEvent,
        "[3:50:25 PM]   has disconnected",
      ),
      (
        HumanConnectionLostLightEvent,
        "[3:50:25 PM]  has disconnected",
      ),
      (
        HumanReturnedToBriefingEvent,
        "[3:50:25 PM] TheUser entered refly menu",
      ),
      (
        HumanReturnedToBriefingEvent,
        "[3:50:25 PM]  The User  entered refly menu",
      ),
      (
        HumanReturnedToBriefingEvent,
        "[3:50:25 PM]   entered refly menu",
      ),
      (
        HumanReturnedToBriefingEvent,
        "[3:50:25 PM]  entered refly menu",
      ),
      (
        HumanSelectedAirfieldEvent,
        "[6:55:50 PM] TheUser selected army Red at 134055.0 136158.0",
      ),
      (
        HumanSelectedAirfieldEvent,
        "[6:55:50 PM] TheUser selected army Red at 134055.0 136158.0 0.0",
      ),
      (
        HumanSelectedAirfieldEvent,
        "[6:55:50 PM]  The User  selected army Red at 134055.0 136158.0 0.0",
      ),
      (
        HumanSelectedAirfieldEvent,
        "[6:55:50 PM]   selected army Red at 134055.0 136158.0 0.0",
      ),
      (
        HumanSelectedAirfieldEvent,
        "[6:55:50 PM]  selected army Red at 134055.0 136158.0 0.0",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM] TheUser started NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM] TheUser stopped NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]  The User  started NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]  The User  stopped NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]   started NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]   stopped NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]  started NTRK record",
      ),
      (
        HumanToggledRecordingEvent,
        "[3:46:16 PM]  stopped NTRK record",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned landing lights on at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned landing lights off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM]  The User :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM]  :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledLandingLightsEvent,
        "[3:50:25 PM] :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM] TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM]  The User :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM]  :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftToggledWingtipSmokesEvent,
        "[3:50:25 PM] :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftSpawnedEvent,
        "[3:50:25 PM] TheUser:Pe-2series84 loaded weapons '2fab500' fuel 50%",
      ),
      (
        HumanAircraftSpawnedEvent,
        "[3:50:25 PM]  The User :Pe-2series84 loaded weapons '2fab500' fuel 50%",
      ),
      (
        HumanAircraftSpawnedEvent,
        "[3:50:25 PM]  :Pe-2series84 loaded weapons '2fab500' fuel 50%",
      ),
      (
        HumanAircraftSpawnedEvent,
        "[3:50:25 PM] :Pe-2series84 loaded weapons '2fab500' fuel 50%",
      ),
      (
        HumanAircraftDespawnedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F removed at 145663.6 62799.64",
      ),
      (
        HumanAircraftDespawnedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F removed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftDespawnedEvent,
        "[3:50:25 PM]  The User :TB-7_M40F removed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftDespawnedEvent,
        "[3:50:25 PM]  :TB-7_M40F removed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftDespawnedEvent,
        "[3:50:25 PM] :TB-7_M40F removed at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftDespawnedEvent,
        "[3:50:25 PM] r01200 removed at 145663.6 62799.64",
      ),
      (
        AIAircraftDespawnedEvent,
        "[3:50:25 PM] r01200 removed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftTookOffEvent,
        "[3:50:25 PM] TheUser:P-39D2 in flight at 91600.414 73098.805",
      ),
      (
        HumanAircraftTookOffEvent,
        "[3:50:25 PM] TheUser:P-39D2 in flight at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftTookOffEvent,
        "[3:50:25 PM]  The User :P-39D2 in flight at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftTookOffEvent,
        "[3:50:25 PM]  :P-39D2 in flight at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftTookOffEvent,
        "[3:50:25 PM] :P-39D2 in flight at 91600.414 73098.805 661.9586",
      ),
      (
        HumanOccupiedCrewMemberSeatEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F(2) seat occupied by TheUser at 91600.414 73098.805 661.9586",
      ),
      (
        HumanOccupiedCrewMemberSeatEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F(2) seat occupied by TheUser at 91600.414 73098.805",
      ),
      (
        HumanOccupiedCrewMemberSeatEvent,
        "[3:50:25 PM]  The User :TB-7_M40F(2) seat occupied by  The User  at 91600.414 73098.805 661.9586",
      ),
      (
        HumanOccupiedCrewMemberSeatEvent,
        "[3:50:25 PM]  :TB-7_M40F(2) seat occupied by   at 91600.414 73098.805 661.9586",
      ),
      (
        HumanOccupiedCrewMemberSeatEvent,
        "[3:50:25 PM] :TB-7_M40F(2) seat occupied by  at 91600.414 73098.805 661.9586",
      ),
      (
        HumanAircraftLandedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F landed at 145663.6 62799.64",
      ),
      (
        HumanAircraftLandedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F landed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftLandedEvent,
        "[3:50:25 PM]  The User :TB-7_M40F landed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftLandedEvent,
        "[3:50:25 PM]  :TB-7_M40F landed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftLandedEvent,
        "[3:50:25 PM] :TB-7_M40F landed at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftLandedEvent,
        "[3:50:25 PM] r01200 landed at 145663.6 62799.64",
      ),
      (
        AIAircraftLandedEvent,
        "[3:50:25 PM] r01200 landed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftCrashedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F crashed at 145663.6 62799.64",
      ),
      (
        HumanAircraftCrashedEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F crashed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftCrashedEvent,
        "[3:50:25 PM]  The User :TB-7_M40F crashed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftCrashedEvent,
        "[3:50:25 PM]  :TB-7_M40F crashed at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftCrashedEvent,
        "[3:50:25 PM] :TB-7_M40F crashed at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftCrashedEvent,
        "[3:50:25 PM] r01200 crashed at 145663.6 62799.64",
      ),
      (
        AIAircraftCrashedEvent,
        "[3:50:25 PM] r01200 crashed at 145663.6 62799.64 83.96088",
      ),
      (
        StationaryUnitCrashedEvent,
        "[3:50:25 PM] 0_Static crashed at 145663.6 62799.64",
      ),
      (
        StationaryUnitCrashedEvent,
        "[3:50:25 PM] 0_Static crashed at 145663.6 62799.64 83.96088",
      ),
      (
        MovingUnitCrashedEvent,
        "[3:50:25 PM] 0_Chief crashed at 145663.6 62799.64",
      ),
      (
        MovingUnitCrashedEvent,
        "[3:50:25 PM] 0_Chief crashed at 145663.6 62799.64 83.96088",
      ),
      (
        MovingUnitMemberCrashedEvent,
        "[3:50:25 PM] 0_Chief1 crashed at 145663.6 62799.64",
      ),
      (
        MovingUnitMemberCrashedEvent,
        "[3:50:25 PM] 0_Chief1 crashed at 145663.6 62799.64 83.96088",
      ),

      (
        AIAircraftShotdownEvent,
        "[3:50:25 PM] r01001 shot down by  at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownEvent,
        "[3:50:25 PM] r01001 shot down by  at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownSelfEvent,
        "[3:50:25 PM] r01001 shot down by landscape at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownSelfEvent,
        "[3:50:25 PM] r01001 shot down by landscape at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownSelfEvent,
        "[3:50:25 PM] r01001 shot down by NONAME at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownSelfEvent,
        "[3:50:25 PM] r01001 shot down by NONAME at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByBridgeEvent,
        "[3:50:25 PM] r01001 shot down by  Bridge159 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByBridgeEvent,
        "[3:50:25 PM] r01001 shot down by  Bridge159 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByBuildingEvent,
        "[3:50:25 PM] r01001 shot down by 194_bld at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByBuildingEvent,
        "[3:50:25 PM] r01001 shot down by 194_bld at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM] r01001 shot down by 0_Chief at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM] r01001 shot down by 0_Chief at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM] r01001 shot down by 0_Chief0 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM] r01001 shot down by 0_Chief0 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByObjectEvent,
        "[3:50:25 PM] r01001 shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByObjectEvent,
        "[3:50:25 PM] r01001 shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM] r01001 shot down by _para_1 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM] r01001 shot down by _para_1 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM] r01001 shot down by 1240_Static at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM] r01001 shot down by 1240_Static at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByTreeEvent,
        "[3:50:25 PM] r01001 shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByTreeEvent,
        "[3:50:25 PM] r01001 shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  The User :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and g01003 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByAIAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and g01003 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and TheUser:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and TheUser:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and  The User :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by g01002 and :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F and g01002 at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  The User :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] r01001 shot down by :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by TheUser:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  The User :TB-7_M40F and  The User2 :TB-7_M40F  at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by  :TB-7_M40F and  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] r01001 shot down by :TB-7_M40F and :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by landscape at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by NONAME at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownSelfEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBridgeEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByBridgeEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBridgeEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBridgeEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBridgeEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBuildingEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 194_bld at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByBuildingEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBuildingEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBuildingEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByBuildingEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 0_Chief at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByMovingUnitMemberEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByObjectEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByObjectEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByObjectEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByObjectEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByObjectEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by _para_1 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByParatrooperEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 1240_Static at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByStationaryUnitEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByTreeEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByTreeEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByTreeEvent,
        "[3:50:25 PM]  The User :TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByTreeEvent,
        "[3:50:25 PM]  :TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByTreeEvent,
        "[3:50:25 PM] :TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and g01003 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and g01003 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and TheUser2:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by g01002 and :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and g01002 at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  The User :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  The User :TB-7_M40F and  The User :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by  :TB-7_M40F and  :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
      (
        HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent,
        "[3:50:25 PM] TheUser:TB-7_M40F shot down by :TB-7_M40F and :TB-7_M40F at 145663.6 62799.64 83.96088",
      ),
    ]

    for cls, line in items:
      try:
        result = parser.parse_line(line)
      except Exception as e:
        raise Exception((cls, line)) from e
      else:
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
