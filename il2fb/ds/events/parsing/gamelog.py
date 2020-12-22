import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from typing import Optional

from .base import CompositeLineWithTimestampParser
from .base import LineWithTimestampParser

from .briefing import HumanReturnedToBriefingLineParser
from .briefing import HumanSelectedAirfieldLineParser

from .connection import HumanConnectionEstablishedLightLineParser
from .connection import HumanConnectionLostLightLineParser

from .crashing import ActorCrashedLineParser

from .landing import ActorLandedLineParser
from .lights import HumanAircraftToggledLandingLightsEventLineParser

from .mission import MissionLoadedLineParser
from .mission import MissionStartedLineParser
from .mission import MissionEndedLineParser
from .mission import MissionWonLineParser

from .recording import HumanToggledRecordingLineParser
from .seats import HumanOccupiedCrewMemberSeatLineParser
from .shootdowns import ActorShotdownLineParser
from .smokes import HumanAircraftToggledWingtipSmokesLineParser

from .spawning import HumanAircraftSpawnedLineParser
from .spawning import ActorDespawnedLineParser

from .takeoff import HumanAircraftTookOffLineParser

from ._utils import export


DEFAULT_GAMELOG_SUBPARSER_CLASSES = (
  HumanOccupiedCrewMemberSeatLineParser,
  HumanAircraftToggledWingtipSmokesLineParser,
  HumanAircraftSpawnedLineParser,
  HumanReturnedToBriefingLineParser,
  HumanSelectedAirfieldLineParser,
  HumanAircraftTookOffLineParser,
  ActorLandedLineParser,
  HumanConnectionEstablishedLightLineParser,
  HumanConnectionLostLightLineParser,
  ActorShotdownLineParser,
  ActorCrashedLineParser,
  MissionLoadedLineParser,
  MissionStartedLineParser,
  MissionEndedLineParser,
  HumanToggledRecordingLineParser,
  HumanAircraftToggledLandingLightsEventLineParser,
  ActorDespawnedLineParser,
  MissionWonLineParser,
)


@export
class GamelogLineParser(CompositeLineWithTimestampParser):

  def __init__(self, subparsers: Optional[Iterable[LineWithTimestampParser]] = None) -> None:
    if not subparsers:
      subparsers = [cls() for cls in DEFAULT_GAMELOG_SUBPARSER_CLASSES]

    super().__init__(subparsers)
