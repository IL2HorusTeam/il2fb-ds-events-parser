import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.lights import HumanToggledLandingLightsEvent
from il2fb.ds.events.definitions.lights import HumanToggledLandingLightsInfo

from .base import LineWithTimestampParser
from .regex import POS_REGEX
from .text import strip_spaces

from ._utils import export


STATE_ON_LITERAL  = "on"
STATE_OFF_LITERAL = "off"

HUMAN_TOGGLED_LANDING_LIGHTS_REGEX = re.compile(
  rf"^(?P<callsign>.*):(?P<aircraft>.+) turned landing lights (?P<state>{STATE_ON_LITERAL}|{STATE_OFF_LITERAL}) at {POS_REGEX}$"
)


@export
class HumanToggledLandingLightsLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about landing lights events.

  Examples of input lines:

    "TheUser:P-39D2 turned landing lights on at 91600.414 73098.805"
    "TheUser:P-39D2 turned landing lights off at 91600.414 73098.805"
    "TheUser:P-39D2 turned landing lights on at 91600.414 73098.805 661.9586"
    "TheUser:P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"
    " The User :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"
    " :P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"
    ":P-39D2 turned landing lights off at 91600.414 73098.805 661.9586"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanToggledLandingLightsEvent]:
    match = HUMAN_TOGGLED_LANDING_LIGHTS_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    actor = HumanAircraftActor(
      callsign=callsign,
      aircraft=match.group('aircraft'),
    )

    state = (match.group('state') == STATE_ON_LITERAL)

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanToggledLandingLightsEvent(HumanToggledLandingLightsInfo(
      timestamp=timestamp,
      actor=actor,
      state=state,
      pos=pos,
    ))
