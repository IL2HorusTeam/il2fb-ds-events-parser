import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.takeoff import HumanAircraftTookOffEvent
from il2fb.ds.events.definitions.takeoff import HumanAircraftTookOffInfo

from .base import LineWithTimestampParser
from .text import strip_spaces

from .regex import HUMAN_AIRCRAFT_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_AIRCRAFT_TOOK_OFF_REGEX = re.compile(
  rf"^{HUMAN_AIRCRAFT_REGEX} in flight at {POS_REGEX}$"
)


@export
class HumanAircraftTookOffLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about take-off events.

  Examples of input lines:

    "TheUser:TB-7_M40F in flight at 145663.6 62799.64"
    "TheUser:TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    " :TB-7_M40F in flight at 145663.6 62799.64 83.96088"
    ":TB-7_M40F in flight at 145663.6 62799.64 83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanAircraftTookOffEvent]:
    match = HUMAN_AIRCRAFT_TOOK_OFF_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    actor = HumanAircraftActor(
      callsign=callsign,
      aircraft=match.group('aircraft'),
    )

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanAircraftTookOffEvent(HumanAircraftTookOffInfo(
      timestamp=timestamp,
      actor=actor,
      pos=pos,
    ))
