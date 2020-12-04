import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.smokes import HumanToggledWingtipSmokesEvent
from il2fb.ds.events.definitions.smokes import HumanToggledWingtipSmokesInfo

from .base import LineWithTimestampParser
from .regex import POS_REGEX

from ._utils import export


STATE_ON_LITERAL  = "on"
STATE_OFF_LITERAL = "off"

HUMAN_TOGGLED_WINGTIP_SMOKES_REGEX = re.compile(
  rf"^(?P<callsign>.+):(?P<aircraft>.+) turned wingtip smokes (?P<state>{STATE_ON_LITERAL}|{STATE_OFF_LITERAL}) at {POS_REGEX}$"
)


@export
class HumanToggledWingtipSmokesLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about wingtip smokes events.

  Examples of input lines:

    "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805 661.9586"
    "TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805 661.9586"
    "TheUser:P-39D2 turned wingtip smokes on at 91600.414 73098.805"
    "TheUser:P-39D2 turned wingtip smokes off at 91600.414 73098.805"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanToggledWingtipSmokesEvent]:
    match = HUMAN_TOGGLED_WINGTIP_SMOKES_REGEX.match(line)
    if not match:
      return

    actor = HumanAircraftActor(
      callsign=match.group('callsign'),
      aircraft=match.group('aircraft'),
    )

    state = (match.group('state') == STATE_ON_LITERAL)

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanToggledWingtipSmokesEvent(HumanToggledWingtipSmokesInfo(
      timestamp=timestamp,
      actor=actor,
      state=state,
      pos=pos,
    ))
