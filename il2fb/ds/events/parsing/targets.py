import datetime

from typing import Optional

from il2fb.commons.targets import TARGET_STATES

from il2fb.ds.events.definitions.targets import TargetStateChangedEvent
from il2fb.ds.events.definitions.targets import TargetStateChangedInfo

from .base import LineWithTimestampParser

from ._utils import export


TARGET_STATE_CHANGED_PREFIX     = "Target "
TARGET_STATE_CHANGED_PREFIX_LEN = len(TARGET_STATE_CHANGED_PREFIX)


@export
class TargetStateChangedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about changes in states of target.

  Examples of input lines:

    "Target 3 Complete"
    "Target 4 Failed"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[TargetStateChangedEvent]:
    if line.startswith(TARGET_STATE_CHANGED_PREFIX):
      index, state = line[TARGET_STATE_CHANGED_PREFIX_LEN:].split(' ', maxsplit=1)

      index = int(index)
      state = TARGET_STATES[state.upper()]

      return TargetStateChangedEvent(TargetStateChangedInfo(
        timestamp=timestamp,
        index=index,
        state=state,
      ))
