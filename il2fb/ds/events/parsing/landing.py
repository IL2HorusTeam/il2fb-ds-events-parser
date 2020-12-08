import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.landing import LandingEvent

from il2fb.ds.events.definitions.landing import AIAircraftLandedEvent
from il2fb.ds.events.definitions.landing import AIAircraftLandedInfo

from il2fb.ds.events.definitions.landing import HumanAircraftLandedEvent
from il2fb.ds.events.definitions.landing import HumanAircraftLandedInfo

from .actors import maybe_HumanAircraftActor_from_id
from .actors import maybe_AIAircraftActor_from_id

from .base import LineWithTimestampParser

from .regex import ACTOR_REGEX
from .regex import POS_REGEX

from ._utils import export


ACTOR_LANDED_REGEX = re.compile(
  rf"^{ACTOR_REGEX} landed at {POS_REGEX}$"
)


@export
class ActorLandedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about landing events.

  Examples of input lines:

    "TheUser:TB-7_M40F landed at 145663.6 62799.64"
    "TheUser:TB-7_M40F landed at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F landed at 145663.6 62799.64 83.96088"
    " :TB-7_M40F landed at 145663.6 62799.64 83.96088"
    ":TB-7_M40F landed at 145663.6 62799.64 83.96088"
    "r01001 landed at 21843.232 195704.28"
    "r01001 landed at 21843.232 195704.28 83.96088"

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

    actor_id = match.group('actor')

    if (actor := maybe_HumanAircraftActor_from_id(actor_id)):
      return HumanAircraftLandedEvent(HumanAircraftLandedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_AIAircraftActor_from_id(actor_id)):
      return AIAircraftLandedEvent(AIAircraftLandedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))
