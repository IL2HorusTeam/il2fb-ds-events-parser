import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanActor
from il2fb.commons.actors import HumanAircraftCrewMemberActor

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.seats import HumanOccupiedCrewMemberSeatEvent
from il2fb.ds.events.definitions.seats import HumanOccupiedCrewMemberSeatInfo

from .base import LineWithTimestampParser
from .text import strip_spaces

from .regex import TARGET_HUMAN_AIRCRAFT_CREW_MEMBER_REGEX
from .regex import CALLSIGN_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_OCCUPIED_CREW_MEMBER_SEAT_REGEX = re.compile(
  rf"^{TARGET_HUMAN_AIRCRAFT_CREW_MEMBER_REGEX} seat occupied by {CALLSIGN_REGEX} at {POS_REGEX}$"
)


@export
class HumanOccupiedCrewMemberSeatLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about wingtip smokes events.

  Examples of input lines:

    "TheUser:TB-7_M40F(2) seat occupied by TheUser at 145663.6 62799.64"
    "TheUser:TB-7_M40F(2) seat occupied by TheUser at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F(2) seat occupied by  The User  at 145663.6 62799.64 83.96088"
    " :TB-7_M40F(2) seat occupied by   at 145663.6 62799.64 83.96088"
    ":TB-7_M40F(2) seat occupied by  at 145663.6 62799.64 83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanOccupiedCrewMemberSeatEvent]:
    match = HUMAN_OCCUPIED_CREW_MEMBER_SEAT_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    actor = HumanActor(
      callsign=callsign,
    )

    target_callsign = strip_spaces(match.group('target_callsign'))
    target = HumanAircraftCrewMemberActor(
      callsign=target_callsign,
      aircraft=match.group('target_aircraft'),
      member_index=int(match.group('target_member_index')),
    )

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanOccupiedCrewMemberSeatEvent(HumanOccupiedCrewMemberSeatInfo(
      timestamp=timestamp,
      actor=actor,
      target=target,
      pos=pos,
    ))
