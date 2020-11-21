import re

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.connection import ChannelInfo
from il2fb.ds.events.definitions.connection import HumanConnectionStartedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightInfo

from il2fb.ds.events.definitions.connection import HumanConnectionStartedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent

from .base import SimpleLineParser
from .datetime import parse_time_or_fail

from ._utils import export


HUMAN_CONNECTION_STARTED_EVENT_REGEX = re.compile(
  r"^socket channel '(?P<channel_no>\d+)' start creating: (?P<address>.+):(?P<port>\d+)$"
)
HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX = re.compile(
  r"^socket channel '(?P<channel_no>\d+)', ip (?P<address>.+):(?P<port>\d+), (?P<callsign>.+), is complete created$"
)
HUMAN_CONNECTION_ESTABLISHED_LIGHT_REGEX = re.compile(
  r"^\[(?P<time>.+)\] (?P<callsign>.+) has connected$"
)
HUMAN_CONNECTION_LOST_EVENT_REGEX = re.compile(
  r"^socketConnection with (?P<address>.+):(?P<port>\d+) on channel (?P<channel_no>\d+) lost.  Reason:(?P<reason>.*)$"
)
HUMAN_CONNECTION_LOST_LIGHT_REGEX = re.compile(
  r"^\[(?P<time>.+)\] (?P<callsign>.+) has disconnected$"
)


@export
class HumanConnectionStartedLineParser(SimpleLineParser):
  """
  Parses console messages about start of a human connection.

  Examples of input lines:

    "socket channel '705' start creating: 127.0.0.1:21000"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionStartedEvent]:
    match = HUMAN_CONNECTION_STARTED_EVENT_REGEX.match(line)
    if not match:
      return

    group      = match.groupdict()
    channel_no = int(group['channel_no'])
    port       = int(group['port'])
    address    = group['address']

    return HumanConnectionStartedEvent(HumanConnectionStartedInfo(
      channel_info=ChannelInfo(
        channel_no=channel_no,
        address=address,
        port=port,
      ),
    ))


@export
class HumanConnectionEstablishedLineParser(SimpleLineParser):
  """
  Parses console messages about establishing of a human connection.

  Examples of input lines:

    "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionEstablishedEvent]:
    match = HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX.match(line)
    if not match:
      return

    group      = match.groupdict()
    channel_no = int(group['channel_no'])
    port       = int(group['port'])
    address    = group['address']
    callsign   = group['callsign']

    return HumanConnectionEstablishedEvent(HumanConnectionEstablishedInfo(
      channel_info=ChannelInfo(
        channel_no=channel_no,
        address=address,
        port=port,
      ),
      actor=HumanActor(callsign),
    ))


@export
class HumanConnectionEstablishedLightLineParser(SimpleLineParser):
  """
  Parses game log messages about establishing of a human connection.

  Examples of input lines:

    "[6:36:45 PM] TheUser has connected"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionEstablishedLightEvent]:
    match = HUMAN_CONNECTION_ESTABLISHED_LIGHT_REGEX.match(line)
    if not match:
      return

    group    = match.groupdict()
    callsign = group['callsign']
    time     = group['time']
    time     = parse_time_or_fail(time)

    return HumanConnectionEstablishedLightEvent(HumanConnectionEstablishedLightInfo(
      time=time,
      actor=HumanActor(callsign),
    ))


@export
class HumanConnectionLostLineParser(SimpleLineParser):
  """
  Parses console messages about loss of a human connection.

  Examples of input lines:

    "socketConnection with 127.0.0.1:60500 on channel 709 lost.  Reason: You have been kicked from the server."
    "socketConnection with 127.0.0.1:21000 on channel 703 lost.  Reason:"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionLostEvent]:
    match = HUMAN_CONNECTION_LOST_EVENT_REGEX.match(line)
    if not match:
      return

    group      = match.groupdict()
    channel_no = int(group['channel_no'])
    port       = int(group['port'])
    address    = group['address']

    reason = group['reason']
    if reason is not None:
      reason = reason.strip()

    reason = reason or None

    return HumanConnectionLostEvent(HumanConnectionLostInfo(
      channel_info=ChannelInfo(
        channel_no=channel_no,
        address=address,
        port=port,
      ),
      reason=reason,
    ))


@export
class HumanConnectionLostLightLineParser(SimpleLineParser):
  """
  Parses game log messages about loss of a human connection.

  Examples of input lines:

    "[9:14:48 PM] TheUser has disconnected"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionLostLightEvent]:
    match = HUMAN_CONNECTION_LOST_LIGHT_REGEX.match(line)
    if not match:
      return

    group    = match.groupdict()
    callsign = group['callsign']
    time     = group['time']
    time     = parse_time_or_fail(time)

    return HumanConnectionLostLightEvent(HumanConnectionLostLightInfo(
      time=time,
      actor=HumanActor(callsign),
    ))
