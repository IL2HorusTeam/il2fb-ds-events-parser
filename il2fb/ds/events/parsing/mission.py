import datetime
import re

from pathlib import Path

from typing import Optional

from il2fb.ds.events.definitions.mission import MissionLoadedInfo
from il2fb.ds.events.definitions.mission import MissionStartedInfo
from il2fb.ds.events.definitions.mission import MissionEndedInfo

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent

from .base import LineWithDatetimeParser
from .base import LineWithTimeParser

from ._utils import export


MISSION_LOADED_EVENT_REGEX = re.compile(
  r"^Mission: (?P<file_path>.+\.mis) is Playing$"
)

MISSION_STARTED_EVENT_LITERAL = "Mission BEGIN"
MISSION_ENDED_EVENT_LITERAL   = "Mission END"


@export
class MissionLoadedLineParser(LineWithDatetimeParser):
  """
  Parses gamelog messages about loaded missions.

  Examples of input lines:

    "Mission: net/dogfight/1596469535.mis is Playing"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[MissionLoadedEvent]:
    match = MISSION_LOADED_EVENT_REGEX.match(line)
    if not match:
      return

    file_path = Path(match.group('file_path'))

    return MissionLoadedEvent(MissionLoadedInfo(
      timestamp=timestamp,
      file_path=file_path,
    ))


@export
class MissionStartedLineParser(LineWithTimeParser):
  """
  Parses gamelog messages about started missions.

  Examples of input lines:

    "Mission BEGIN"

  """
  def parse_line(self, timestamp: datetime.time, line: str) -> Optional[MissionStartedEvent]:
    if line == MISSION_STARTED_EVENT_LITERAL:
      return MissionStartedEvent(MissionStartedInfo(timestamp=timestamp))


@export
class MissionEndedLineParser(LineWithTimeParser):
  """
  Parses gamelog messages about ended missions.

  Examples of input lines:

    "Mission END"

  """
  def parse_line(self, timestamp: datetime.time, line: str) -> Optional[MissionEndedEvent]:
    if line == MISSION_ENDED_EVENT_LITERAL:
      return MissionEndedEvent(MissionEndedInfo(timestamp=timestamp))
