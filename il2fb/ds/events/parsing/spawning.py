import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedInfo

from .base import LineWithTimestampParser
from .text import strip_spaces

from .regex import AIRCRAFT_REGEX
from .regex import CALLSIGN_REGEX
from .regex import POS_REGEX

from ._utils import export


PERCENT_LITERAL = "%"

HUMAN_AIRCRAFT_SPAWNED_REGEX = re.compile(
  rf"^{CALLSIGN_REGEX}:{AIRCRAFT_REGEX} loaded weapons '(?P<weapons>.+)' fuel (?P<fuel>\d+){PERCENT_LITERAL}$"
)


@export
class HumanAircraftSpawnedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about spawned human aircrafts.

  Examples of input lines:

    "TheUser:Pe-2series84 loaded weapons '2fab500' fuel 50%"
    " The User :Pe-2series84 loaded weapons '2fab500' fuel 50%"
    " :Pe-2series84 loaded weapons '2fab500' fuel 50%"
    ":Pe-2series84 loaded weapons '2fab500' fuel 50%"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanAircraftSpawnedEvent]:
    if not line.endswith(PERCENT_LITERAL):
      return

    match = HUMAN_AIRCRAFT_SPAWNED_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    actor = HumanAircraftActor(
      callsign=callsign,
      aircraft=match.group('aircraft'),
    )

    fuel = int(match.group('fuel'))

    return HumanAircraftSpawnedEvent(HumanAircraftSpawnedInfo(
      timestamp=timestamp,
      actor=actor,
      weapons=match.group('weapons'),
      fuel=fuel,
    ))
