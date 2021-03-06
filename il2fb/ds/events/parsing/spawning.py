import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.spawning import DespawningEvent

from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftSpawnedInfo

from il2fb.ds.events.definitions.spawning import HumanAircraftDespawnedEvent
from il2fb.ds.events.definitions.spawning import HumanAircraftDespawnedInfo

from il2fb.ds.events.definitions.spawning import AIAircraftDespawnedEvent
from il2fb.ds.events.definitions.spawning import AIAircraftDespawnedInfo

from .actors import maybe_HumanAircraftActor_from_id
from .actors import maybe_AIAircraftActor_from_id

from .base import LineWithTimestampParser
from .literals import PERCENT_LITERAL
from .text import strip_spaces

from .regex import ACTOR_REGEX
from .regex import HUMAN_AIRCRAFT_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_AIRCRAFT_SPAWNED_REGEX = re.compile(
  rf"^{HUMAN_AIRCRAFT_REGEX} loaded weapons '(?P<weapons>.+)' fuel (?P<fuel>\d+){PERCENT_LITERAL}$"
)

ACTOR_DESPAWNED_REGEX = re.compile(
  rf"^{ACTOR_REGEX} removed at {POS_REGEX}$"
)


@export
class HumanAircraftSpawnedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about spawned human aircrafts.

  Examples of input lines:

    "TheUser:TB-7_M40F removed at 145663.6 62799.64"
    "TheUser:TB-7_M40F removed at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    " :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    ":TB-7_M40F removed at 145663.6 62799.64 83.96088"

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


@export
class ActorDespawnedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about despawned aircrafts.

  Examples of input lines:

    "TheUser:TB-7_M40F removed at 145663.6 62799.64"
    "TheUser:TB-7_M40F removed at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    " :TB-7_M40F removed at 145663.6 62799.64 83.96088"
    ":TB-7_M40F removed at 145663.6 62799.64 83.96088"
    "r01200 removed at 145663.6 62799.64"
    "r01200 removed at 145663.6 62799.64 83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[DespawningEvent]:
    match = ACTOR_DESPAWNED_REGEX.match(line)
    if not match:
      return

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    actor_id = match.group('actor')

    if (actor := maybe_HumanAircraftActor_from_id(actor_id)):
      return HumanAircraftDespawnedEvent(HumanAircraftDespawnedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_AIAircraftActor_from_id(actor_id)):
      return AIAircraftDespawnedEvent(AIAircraftDespawnedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))
