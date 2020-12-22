import datetime
import re

from pathlib import Path

from typing import Optional

from il2fb.commons.belligerents import BELLIGERENTS

from il2fb.ds.events.definitions.mission import MissionLoadedInfo
from il2fb.ds.events.definitions.mission import MissionStartedInfo
from il2fb.ds.events.definitions.mission import MissionEndedInfo
from il2fb.ds.events.definitions.mission import MissionWonInfo

from il2fb.ds.events.definitions.mission import MissionLoadedEvent
from il2fb.ds.events.definitions.mission import MissionStartedEvent
from il2fb.ds.events.definitions.mission import MissionEndedEvent
from il2fb.ds.events.definitions.mission import MissionWonEvent

from .base import LineWithTimestampParser
from .regex import BELLIGERENT_REGEX

from ._utils import export


MISSION_LOADED_EVENT_REGEX = re.compile(
  r"^Mission: (?P<file_path>.+\.mis) is Playing$"
)

MISSION_WON_EVENT_REGEX = re.compile(
  rf"^Mission: {BELLIGERENT_REGEX} WON$"
)

MISSION_STARTED_EVENT_LITERAL = "Mission BEGIN"
MISSION_ENDED_EVENT_LITERAL   = "Mission END"


@export
class MissionLoadedLineParser(LineWithTimestampParser):
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
class MissionStartedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about started missions.

  Examples of input lines:

    "Mission BEGIN"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[MissionStartedEvent]:
    if line == MISSION_STARTED_EVENT_LITERAL:
      return MissionStartedEvent(MissionStartedInfo(timestamp=timestamp))


@export
class MissionEndedLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about ended missions.

  Examples of input lines:

    "Mission END"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[MissionEndedEvent]:
    if line == MISSION_ENDED_EVENT_LITERAL:
      return MissionEndedEvent(MissionEndedInfo(timestamp=timestamp))


@export
class MissionWonLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about loaded missions.

  Examples of input lines:

    "Mission: RED WON"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[MissionWonEvent]:
    match = MISSION_WON_EVENT_REGEX.match(line)
    if not match:
      return

    belligerent = match.group('belligerent').upper()
    belligerent = BELLIGERENTS[belligerent]

    return MissionWonEvent(MissionWonInfo(
      timestamp=timestamp,
      belligerent=belligerent,
    ))
