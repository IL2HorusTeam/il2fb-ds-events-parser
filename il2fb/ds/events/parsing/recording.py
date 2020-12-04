import datetime

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent
from il2fb.ds.events.definitions.recording import HumanToggledRecordingInfo

from .base import LineWithTimestampParser
from .text import strip_spaces

from ._utils import export


RECORDING_ON_LITERAL  = "started"
RECORDING_OFF_LITERAL = "stopped"

HUMAN_TOGGLED_RECORDING_SUFFIX     = " NTRK record"
HUMAN_TOGGLED_RECORDING_SUFFIX_LEN = len(HUMAN_TOGGLED_RECORDING_SUFFIX)


@export
class HumanToggledRecordingLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about track recording events.

  Examples of input lines:

    "TheUser started NTRK record"
    "TheUser stopped NTRK record"
    " The User  started NTRK record"
    " The User  stopped NTRK record"
    "  started NTRK record"
    "  stopped NTRK record"
    " started NTRK record"
    " stopped NTRK record"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanToggledRecordingEvent]:
    if not line.endswith(HUMAN_TOGGLED_RECORDING_SUFFIX):
      return

    callsign, action = line[:-HUMAN_TOGGLED_RECORDING_SUFFIX_LEN].rsplit(" ", 1)

    callsign = strip_spaces(callsign)
    state    = (action == RECORDING_ON_LITERAL)

    return HumanToggledRecordingEvent(HumanToggledRecordingInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
      state=state,
    ))
