import re

from typing import Optional

from il2fb.ds.events.definitions.cheating import CheatingInfo
from il2fb.ds.events.definitions.cheating import CheatingDetectedEvent

from .base import SimpleLineParser

from ._utils import export


CHEATING_REGEX = re.compile(
  r"^socket channel '(?P<channel_no>\d+)' Cheater was detected! Reason=(?P<cheat_code>-?\d+):\s'(?P<cheat_details>.+)'$"
)


@export
class CheatingLineParser(SimpleLineParser):
  """
  Parses cheating detection messages.

  Examples of input lines:

    "socket channel '203' Cheater was detected! Reason=8: 'Cheat-Engine'"
    "socket channel '87' Cheater was detected! Reason=-557645630: 'Unknow'"
    "socket channel '751' Cheater was detected! Reason=118227478: 'Unknow'"
    "socket channel '145' Cheater was detected! Reason=7: 'Il2trainerstable'"

  """

  def parse_line(self, line: str) -> Optional[CheatingDetectedEvent]:
    match = CHEATING_REGEX.match(line)
    if not match:
      return

    group         = match.groupdict()
    channel_no    = int(group['channel_no'])
    cheat_code    = int(group['cheat_code'])
    cheat_details = group['cheat_details']

    return CheatingDetectedEvent(CheatingInfo(
      channel_no=channel_no,
      cheat_code=cheat_code,
      cheat_details=cheat_details,
    ))
