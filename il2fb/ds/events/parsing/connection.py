import re

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.connection import ConnectionAddress

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightInfo
from il2fb.ds.events.definitions.connection import HumanConnectionFailedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightInfo
from il2fb.ds.events.definitions.connection import HumanConnectionStartedInfo

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionFailedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionStartedEvent

from .base import SimpleLineParser
from .timestamps import parse_time_or_fail

from ._utils import export


HUMAN_CONNECTION_STARTED_EVENT_REGEX = re.compile(
  r"^socket channel '(?P<channel_no>\d+)' start creating: (?P<host>.+):(?P<port>\d+)$"
)
HUMAN_CONNECTION_FAILED_EVENT_REGEX = re.compile(
  r"^socket channel NOT created \((?P<reason>.*)\): (?P<host>.+):(?P<port>\d+)$"
)
HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX = re.compile(
  r"^socket channel '(?P<channel_no>\d+)', ip (?P<host>.+):(?P<port>\d+), (?P<callsign>.*), is complete created$"
)
HUMAN_CONNECTION_ESTABLISHED_LIGHT_REGEX = re.compile(
  r"^\[(?P<time>.+)\] (?P<callsign>.+) has connected$"
)
HUMAN_CONNECTION_LOST_EVENT_REGEX = re.compile(
  r"^socketConnection with (?P<host>.+):(?P<port>\d+) on channel (?P<channel_no>\d+) lost.  Reason:(?P<reason>.*)$"
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
    host       = group['host']

    return HumanConnectionStartedEvent(HumanConnectionStartedInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
    ))


@export
class HumanConnectionFailedLineParser(SimpleLineParser):
  """
  Parses console messages about failure of a human connection.

  Examples of input lines:

    "socket channel NOT created (): 127.0.0.1:45292"
    "socket channel NOT created (Only TREE network structure is supported.): 127.0.0.1:21000"
    "socket channel NOT created (Reconnect user): 127.0.0.1:21000"
    "socket channel NOT created (Timeout.): 127.0.0.1:19841"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionFailedEvent]:
    match = HUMAN_CONNECTION_FAILED_EVENT_REGEX.match(line)
    if not match:
      return

    group = match.groupdict()
    port  = int(group['port'])
    host  = group['host']

    reason = group['reason']
    if reason is not None:
      reason = reason.strip()

    reason = reason or None

    return HumanConnectionFailedEvent(HumanConnectionFailedInfo(
      address=ConnectionAddress(host=host, port=port),
      reason=reason,
    ))


@export
class HumanConnectionEstablishedLineParser(SimpleLineParser):
  """
  Parses console messages about establishing of a human connection.

  Examples of input lines:

    "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"
    "socket channel '115', ip 127.0.0.1:4114, , is complete created"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionEstablishedEvent]:
    match = HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX.match(line)
    if not match:
      return

    group      = match.groupdict()
    channel_no = int(group['channel_no'])
    port       = int(group['port'])
    host       = group['host']

    callsign = group['callsign']
    if callsign is not None:
      callsign = callsign.strip()

    actor = HumanActor(callsign) if callsign else None

    return HumanConnectionEstablishedEvent(HumanConnectionEstablishedInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
      actor=actor,
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
    host       = group['host']

    reason = group['reason']
    if reason is not None:
      reason = reason.strip()

    reason = reason or None

    return HumanConnectionLostEvent(HumanConnectionLostInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
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
