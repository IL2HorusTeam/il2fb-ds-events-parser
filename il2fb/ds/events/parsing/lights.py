import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.lights import HumanAircraftToggledLandingLightsEvent
from il2fb.ds.events.definitions.lights import HumanAircraftToggledLandingLightsInfo

from .base import LineWithTimestampParser
from .literals import SWITCH_STATE_ON_LITERAL
from .text import strip_spaces

from .regex import HUMAN_AIRCRAFT_REGEX
from .regex import SWITCH_STATE_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_AIRCRAFT_TOGGLED_LANDING_LIGHTS_REGEX = re.compile(
  rf"^{HUMAN_AIRCRAFT_REGEX} turned landing lights {SWITCH_STATE_REGEX} at {POS_REGEX}$"
)


@export
class HumanAircraftToggledLandingLightsEventLineParser(LineWithTimestampParser):
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
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanAircraftToggledLandingLightsEvent]:
    match = HUMAN_AIRCRAFT_TOGGLED_LANDING_LIGHTS_REGEX.match(line)
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

    return HumanAircraftToggledLandingLightsEvent(HumanAircraftToggledLandingLightsInfo(
      timestamp=timestamp,
      actor=actor,
      state=state,
      pos=pos,
    ))
