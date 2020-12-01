import datetime

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingEvent
from il2fb.ds.events.definitions.briefing import HumanReturnedToBriefingInfo

from .base import LineWithTimeParser

from ._utils import export


RETURNED_TO_BRIEFING_SUFFIX     = " entered refly menu"
RETURNED_TO_BRIEFING_SUFFIX_LEN = len(RETURNED_TO_BRIEFING_SUFFIX)


@export
class HumanReturnedToBriefingLineParser(LineWithTimeParser):
  """
  Parses gamelog messages about users returning to briefing.

  Examples of input lines:

    "TheUser entered refly menu"

  """
  def parse_line(self, timestamp: datetime.time, line: str) -> Optional[HumanReturnedToBriefingEvent]:
    if not line.endswith(RETURNED_TO_BRIEFING_SUFFIX):
      return

    callsign = line[:-RETURNED_TO_BRIEFING_SUFFIX_LEN].rstrip()

    return HumanReturnedToBriefingEvent(HumanReturnedToBriefingInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
    ))
