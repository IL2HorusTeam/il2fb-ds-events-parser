import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.smokes import HumanAircraftToggledWingtipSmokesEvent
from il2fb.ds.events.definitions.smokes import HumanAircraftToggledWingtipSmokesInfo

from .base import LineWithTimestampParser
from .literals import SWITCH_STATE_ON_LITERAL
from .text import strip_spaces

from .regex import HUMAN_AIRCRAFT_REGEX
from .regex import SWITCH_STATE_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_AIRCRAFT_TOGGLED_WINGTIP_SMOKES_REGEX = re.compile(
  rf"^{HUMAN_AIRCRAFT_REGEX} turned wingtip smokes {SWITCH_STATE_REGEX} at {POS_REGEX}$"
)


@export
class HumanAircraftToggledWingtipSmokesLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about wingtip smokes events.

  Examples of input lines:

    "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    "TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"
    "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805"
    "TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805"
    " The User :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"
    " :P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"
    ":P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanAircraftToggledWingtipSmokesEvent]:
    match = HUMAN_AIRCRAFT_TOGGLED_WINGTIP_SMOKES_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    actor = HumanAircraftActor(
      callsign=callsign,
      aircraft=match.group('aircraft'),
    )

    state = (match.group('state') == SWITCH_STATE_ON_LITERAL)

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanAircraftToggledWingtipSmokesEvent(HumanAircraftToggledWingtipSmokesInfo(
      timestamp=timestamp,
      actor=actor,
      state=state,
      pos=pos,
    ))
