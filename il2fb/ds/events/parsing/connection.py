import datetime
import re

from typing import Optional

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.connection import ConnectionAddress

from il2fb.ds.events.definitions.connection import HumanConnectionStartedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionStartedEvent

from il2fb.ds.events.definitions.connection import HumanConnectionFailedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionFailedEvent

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedInfo
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedEvent

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightInfo
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent

from il2fb.ds.events.definitions.connection import HumanConnectionLostInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostEvent

from il2fb.ds.events.definitions.connection import HumanConnectionLostLightInfo
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent


from .base import PlainLineParser
from .base import LineWithTimestampParser
from .text import strip_spaces

from .regex import CALLSIGN_REGEX
from .regex import CHANNEL_NO_REGEX
from .regex import HOST_REGEX
from .regex import PORT_REGEX
from .regex import REASON_REGEX

from ._utils import export


HUMAN_CONNECTION_STARTED_EVENT_REGEX = re.compile(
  rf"^socket channel '{CHANNEL_NO_REGEX}' start creating: {HOST_REGEX}:{PORT_REGEX}$"
)
HUMAN_CONNECTION_FAILED_EVENT_REGEX = re.compile(
  rf"^socket channel NOT created \({REASON_REGEX}\): {HOST_REGEX}:{PORT_REGEX}$"
)
HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX = re.compile(
  rf"^socket channel '{CHANNEL_NO_REGEX}', ip {HOST_REGEX}:{PORT_REGEX}, {CALLSIGN_REGEX}, is complete created$"
)
HUMAN_CONNECTION_LOST_EVENT_REGEX = re.compile(
  rf"^socketConnection with {HOST_REGEX}:{PORT_REGEX} on channel {CHANNEL_NO_REGEX} lost.  Reason: {REASON_REGEX}$"
)

HUMAN_CONNECTION_ESTABLISHED_LIGHT_SUFFIX     = " has connected"
HUMAN_CONNECTION_ESTABLISHED_LIGHT_SUFFIX_LEN = len(HUMAN_CONNECTION_ESTABLISHED_LIGHT_SUFFIX)

HUMAN_CONNECTION_LOST_LIGHT_SUFFIX     = " has disconnected"
HUMAN_CONNECTION_LOST_LIGHT_SUFFIX_LEN = len(HUMAN_CONNECTION_LOST_LIGHT_SUFFIX)


@export
class HumanConnectionStartedLineParser(PlainLineParser):
  """
  Parses console messages about start of a human connection.

  Examples of input lines:

    "socket channel '705' start creating: 127.0.0.1:21000"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionStartedEvent]:
    match = HUMAN_CONNECTION_STARTED_EVENT_REGEX.match(line)
    if not match:
      return

    channel_no = int(match.group('channel_no'))
    port       = int(match.group('port'))
    host       = match.group('host')

    return HumanConnectionStartedEvent(HumanConnectionStartedInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
    ))


@export
class HumanConnectionFailedLineParser(PlainLineParser):
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

    port  = int(match.group('port'))
    host  = match.group('host')

    reason = match.group('reason')
    if reason is not None:
      reason = reason.strip()

    reason = reason or None

    return HumanConnectionFailedEvent(HumanConnectionFailedInfo(
      address=ConnectionAddress(host=host, port=port),
      reason=reason,
    ))


@export
class HumanConnectionEstablishedLineParser(PlainLineParser):
  """
  Parses console messages about establishing of a human connection.

  Examples of input lines:

    "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"
    "socket channel '699', ip 127.0.0.1:21000,  The User , is complete created"
    "socket channel '115', ip 127.0.0.1:4114,   , is complete created"
    "socket channel '115', ip 127.0.0.1:4114, , is complete created"

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionEstablishedEvent]:
    match = HUMAN_CONNECTION_ESTABLISHED_EVENT_REGEX.match(line)
    if not match:
      return

    channel_no = int(match.group('channel_no'))
    port       = int(match.group('port'))
    host       = match.group('host')
    callsign   = strip_spaces(match.group('callsign'))

    return HumanConnectionEstablishedEvent(HumanConnectionEstablishedInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
      actor=HumanActor(callsign=callsign),
    ))


@export
class HumanConnectionEstablishedLightLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about establishing of a human connection.

  Examples of input lines:

    "TheUser has connected"
    " The User  has connected"
    "  has connected"
    " has connected"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanConnectionEstablishedLightEvent]:
    if not line.endswith(HUMAN_CONNECTION_ESTABLISHED_LIGHT_SUFFIX):
      return

    callsign = strip_spaces(line[:-HUMAN_CONNECTION_ESTABLISHED_LIGHT_SUFFIX_LEN])

    return HumanConnectionEstablishedLightEvent(HumanConnectionEstablishedLightInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
    ))


@export
class HumanConnectionLostLineParser(PlainLineParser):
  """
  Parses console messages about loss of a human connection.

  Examples of input lines:

    "socketConnection with 127.0.0.1:60500 on channel 709 lost.  Reason: You have been kicked from the server."
    "socketConnection with 127.0.0.1:21000 on channel 703 lost.  Reason: "

  """
  def parse_line(self, line: str) -> Optional[HumanConnectionLostEvent]:
    match = HUMAN_CONNECTION_LOST_EVENT_REGEX.match(line)
    if not match:
      return

    channel_no = int(match.group('channel_no'))
    port       = int(match.group('port'))
    host       = match.group('host')

    reason = match.group('reason')
    if reason is not None:
      reason = reason.strip()

    reason = reason or None

    return HumanConnectionLostEvent(HumanConnectionLostInfo(
      address=ConnectionAddress(host=host, port=port),
      channel_no=channel_no,
      reason=reason,
    ))


@export
class HumanConnectionLostLightLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about loss of a human connection.

  Examples of input lines:

    "TheUser has disconnected"
    " The User  has disconnected"
    "  has disconnected"
    " has disconnected"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[HumanConnectionLostLightEvent]:
    if not line.endswith(HUMAN_CONNECTION_LOST_LIGHT_SUFFIX):
      return

    callsign = strip_spaces(line[:-HUMAN_CONNECTION_LOST_LIGHT_SUFFIX_LEN])


    return HumanConnectionLostLightEvent(HumanConnectionLostLightInfo(
      timestamp=timestamp,
      actor=HumanActor(callsign=callsign),
    ))
