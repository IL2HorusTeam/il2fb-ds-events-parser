import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanActor
from il2fb.commons.belligerents import BELLIGERENTS
from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldEvent

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingInfo
from il2fb.ds.events.definitions.briefing import HumanSelectedAirfieldInfo

from .base import LineWithTimeParser
from .regex import POS_REGEX

from ._utils import export


HUMAN_RETURNED_TO_BRIEFING_SUFFIX     = " entered refly menu"
HUMAN_RETURNED_TO_BRIEFING_SUFFIX_LEN = len(HUMAN_RETURNED_TO_BRIEFING_SUFFIX)

HUMAN_SELECTED_AIRFIELD_REGEX = re.compile(
  rf"^(?P<callsign>.+) selected army (?P<belligerent>.+) at {POS_REGEX}$"
)


@export
class HumanReturnedToBriefingLineParser(LineWithTimeParser):
  """
  Parses gamelog messages about users returning to briefing.

  Examples of input lines:

    "TheUser entered refly menu"

  """
  def parse_line(self, timestamp: datetime.time, line: str) -> Optional[HumanReturnedToBriefingEvent]:
    if not line.endswith(HUMAN_RETURNED_TO_BRIEFING_SUFFIX):
      return

    callsign = line[:-HUMAN_RETURNED_TO_BRIEFING_SUFFIX_LEN].rstrip()

    return HumanReturnedToBriefingEvent(HumanReturnedToBriefingInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
    ))


@export
class HumanSelectedAirfieldLineParser(LineWithTimeParser):
  """
  Parses gamelog messages about selection of airfields by users.

  Examples of input lines:

    "TheUser selected army Red at 134055.0 136158.0 0.0"
    "TheUser selected army Red at 134055.0 136158.0"

  """
  def parse_line(self, timestamp: datetime.time, line: str) -> Optional[HumanSelectedAirfieldEvent]:
    match = HUMAN_SELECTED_AIRFIELD_REGEX.match(line)
    if not match:
      return

    actor = HumanActor(callsign=match.group('callsign'))

    belligerent = match.group('belligerent').upper()
    belligerent = BELLIGERENTS[belligerent]

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    return HumanSelectedAirfieldEvent(HumanSelectedAirfieldInfo(
      timestamp=timestamp,
      actor=actor,
      belligerent=belligerent,
      pos=pos,
    ))
