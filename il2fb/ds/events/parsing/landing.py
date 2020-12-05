import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.actors import UnknownActor

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.landing import LandingEvent

from il2fb.ds.events.definitions.landing import AIAircraftLandedEvent
from il2fb.ds.events.definitions.landing import AIAircraftLandedInfo

from il2fb.ds.events.definitions.landing import HumanAircraftLandedEvent
from il2fb.ds.events.definitions.landing import HumanAircraftLandedInfo

from il2fb.ds.events.definitions.landing import UnknownActorLandedEvent
from il2fb.ds.events.definitions.landing import UnknownActorLandedInfo

from .actors import maybe_AIAircraftActor_from_id
from .base import LineWithTimestampParser
from .literals import HUMAN_AIRCRAFT_DELIM
from .text import strip_spaces

from .regex import ACTOR_REGEX
from .regex import POS_REGEX

from ._utils import export


ACTOR_LANDED_REGEX = re.compile(
  rf"^{ACTOR_REGEX} landed at {POS_REGEX}$"
)


@export
class AircraftLandedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about landing events.

  Examples of input lines:

    "TheUser:TB-7_M40F in flight at 145663.6 62799.64"
    "TheUser:TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    " :TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    ":TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    "r01001 landed at 21843.232 195704.28"
    "r01001 landed at 21843.232 195704.28  83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[LandingEvent]:
    match = ACTOR_LANDED_REGEX.match(line)
    if not match:
      return

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    actor = match.group('actor')
    if HUMAN_AIRCRAFT_DELIM in actor:
      callsign, aircraft = actor.rsplit(HUMAN_AIRCRAFT_DELIM, 1)
      callsign = strip_spaces(callsign)
      actor = HumanAircraftActor(
        callsign=callsign,
        aircraft=aircraft,
      )
      return HumanAircraftLandedEvent(HumanAircraftLandedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    ai_aircraft = maybe_AIAircraftActor_from_id(actor)
    if ai_aircraft:
      return AIAircraftLandedEvent(AIAircraftLandedInfo(
        timestamp=timestamp,
        actor=ai_aircraft,
        pos=pos,
      ))

    return self._parse_unknown_actor(
      timestamp=timestamp,
      actor=actor,
      pos=pos,
    )

  def _parse_unknown_actor(
    self,
    timestamp: datetime.datetime,
    pos: Point3D,
    actor: str,
  ) ->  Optional[LandingEvent]:
    """Allows customization via overrides"""
    return UnknownActorLandedEvent(UnknownActorLandedInfo(
      timestamp=timestamp,
      actor=UnknownActor(id=actor),
      pos=pos,
    ))