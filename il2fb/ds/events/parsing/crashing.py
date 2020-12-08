import datetime
import re

from typing import Optional

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.crashing import CrashingEvent

from il2fb.ds.events.definitions.crashing import AIAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import AIAircraftCrashedInfo

from il2fb.ds.events.definitions.crashing import HumanAircraftCrashedEvent
from il2fb.ds.events.definitions.crashing import HumanAircraftCrashedInfo

from il2fb.ds.events.definitions.crashing import MovingUnitCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitCrashedInfo

from il2fb.ds.events.definitions.crashing import MovingUnitMemberCrashedEvent
from il2fb.ds.events.definitions.crashing import MovingUnitMemberCrashedInfo

from il2fb.ds.events.definitions.crashing import StationaryUnitCrashedEvent
from il2fb.ds.events.definitions.crashing import StationaryUnitCrashedInfo

from .actors import maybe_AIAircraftActor_from_id
from .actors import maybe_HumanAircraftActor_from_id
from .actors import maybe_MovingUnitActor_from_id
from .actors import maybe_MovingUnitMemberActor_from_id
from .actors import maybe_StationaryUnitActor_from_id

from .base import LineWithTimestampParser

from .regex import ACTOR_REGEX
from .regex import POS_REGEX

from ._utils import export


ACTOR_CRASHED_REGEX = re.compile(
  rf"^{ACTOR_REGEX} crashed at {POS_REGEX}$"
)


@export
class ActorCrashedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about crashes.

  Examples of input lines:

    "TheUser:TB-7_M40F crashed at 145663.6 62799.64"
    "TheUser:TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    " :TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    ":TB-7_M40F crashed at 145663.6 62799.64 83.96088"
    "r01001 crashed at 21843.232 195704.28"
    "r01001 crashed at 21843.232 195704.28 83.96088"
    "0_Chief1 crashed at 21843.232 195704.28"
    "0_Chief1 crashed at 21843.232 195704.28 83.96088"
    "0_Chief crashed at 21843.232 195704.28"
    "0_Chief crashed at 21843.232 195704.28 83.96088"
    "0_Static crashed at 21843.232 195704.28 83.96088"
    "0_Static crashed at 21843.232 195704.28 83.96088 83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[CrashingEvent]:
    match = ACTOR_CRASHED_REGEX.match(line)
    if not match:
      return

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    actor_id = match.group('actor')

    if (actor := maybe_HumanAircraftActor_from_id(actor_id)):
      return HumanAircraftCrashedEvent(HumanAircraftCrashedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_StationaryUnitActor_from_id(actor_id)):
      return StationaryUnitCrashedEvent(StationaryUnitCrashedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_MovingUnitActor_from_id(actor_id)):
      return MovingUnitCrashedEvent(MovingUnitCrashedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_MovingUnitMemberActor_from_id(actor_id)):
      return MovingUnitMemberCrashedEvent(MovingUnitMemberCrashedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))

    if (actor := maybe_AIAircraftActor_from_id(actor_id)):
      return AIAircraftCrashedEvent(AIAircraftCrashedInfo(
        timestamp=timestamp,
        actor=actor,
        pos=pos,
      ))
