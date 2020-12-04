import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.recording import HumanToggledRecordingEvent
from il2fb.ds.events.definitions.recording import HumanToggledRecordingInfo

from .base import LineWithTimestampParser

from ._utils import export


RECORDING_ON_LITERAL  = "started"
RECORDING_OFF_LITERAL = "stopped"

HUMAN_TOGGLED_RECORDING_REGEX = re.compile(
  rf"^((?P<callsign>.*)\s+)?(?P<action>{RECORDING_ON_LITERAL}|{RECORDING_OFF_LITERAL}) NTRK record$"
)


@export
class HumanToggledRecordingLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about track recording events.

  Examples of input lines:

    "TheUser started NTRK record"
    "TheUser stopped NTRK record"
    "started NTRK record"
    "stopped NTRK record"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanToggledRecordingEvent]:
    match = HUMAN_TOGGLED_RECORDING_REGEX.match(line)
    if not match:
      return

    callsign = match.group('callsign')
    if callsign is not None:
      callsign = callsign.strip()

    actor =  HumanActor(callsign) if callsign else None
    state = (match.group('action') == RECORDING_ON_LITERAL)

    return HumanToggledRecordingEvent(HumanToggledRecordingInfo(
      timestamp=timestamp,
      actor=actor,
      state=state,
    ))
