import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanActor
from il2fb.commons.belligerents import BELLIGERENTS
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingInfo

from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldEvent
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldInfo

from .base import LineWithTimestampParser
from .text import strip_spaces

from .regex import BELLIGERENT_REGEX
from .regex import CALLSIGN_REGEX
from .regex import POS_REGEX

from ._utils import export


HUMAN_RETURNED_TO_BRIEFING_SUFFIX     = " entered refly menu"
HUMAN_RETURNED_TO_BRIEFING_SUFFIX_LEN = len(HUMAN_RETURNED_TO_BRIEFING_SUFFIX)

HUMAN_SELECTED_AIRFIELD_REGEX = re.compile(
  rf"^{CALLSIGN_REGEX} selected army {BELLIGERENT_REGEX} at {POS_REGEX}$"
)


@export
class HumanReturnedToBriefingLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about users returning to briefing.

  Examples of input lines:

    "TheUser entered refly menu"
    " The User  entered refly menu"
    "  entered refly menu"
    " entered refly menu"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanReturnedToBriefingEvent]:
    if not line.endswith(HUMAN_RETURNED_TO_BRIEFING_SUFFIX):
      return

    callsign = strip_spaces(line[:-HUMAN_RETURNED_TO_BRIEFING_SUFFIX_LEN])

    return HumanReturnedToBriefingEvent(HumanReturnedToBriefingInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
    ))


@export
class HumanSelectedAirfieldLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about selection of airfields by users.

  Examples of input lines:

    "TheUser selected army Red at 134055.0 136158.0"
    "TheUser selected army Red at 134055.0 136158.0 0.0"
    " The User  selected army Red at 134055.0 136158.0 0.0"
    "  selected army Red at 134055.0 136158.0 0.0"
    " selected army Red at 134055.0 136158.0 0.0"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanSelectedAirfieldEvent]:
    match = HUMAN_SELECTED_AIRFIELD_REGEX.match(line)
    if not match:
      return

    callsign = strip_spaces(match.group('callsign'))

    belligerent = match.group('belligerent').upper()
    belligerent = BELLIGERENTS[belligerent]

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanSelectedAirfieldEvent(HumanSelectedAirfieldInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
      belligerent=belligerent,
      pos=pos,
    ))
