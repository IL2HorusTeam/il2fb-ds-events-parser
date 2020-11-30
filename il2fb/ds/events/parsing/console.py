import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from typing import Optional

from .base import CompositePlainLineParser
from .base import PlainLineParser

from .chat import ChatLineParser
from .cheating import CheatingLineParser

from .connection import HumanConnectionEstablishedLineParser
from .connection import HumanConnectionFailedLineParser
from .connection import HumanConnectionLostLineParser
from .connection import HumanConnectionStartedLineParser

from ._utils import export

# Order affects performance. The following order is based on statistics
# of 600k console events collected during several months of server's execution.
# Comments show percentage of hits per parser.
DEFAULT_CONSOLE_SUBPARSER_CLASSES = [

  # 93.9519%
  #  - ServerChatMessageEvent  83.2624%
  #  - HumanChatMessageEvent    6.1334%
  #  - SystemChatMessageEvent   4.5561%
  ChatLineParser,

  # 2.0003%
  HumanConnectionStartedLineParser,

  # 1.9981%
  HumanConnectionEstablishedLineParser,

  # 1.9919%
  HumanConnectionLostLineParser,

  # 0.0331%
  CheatingLineParser,

  # 0.0246%
  HumanConnectionFailedLineParser,
]


@export
class ConsoleLineParser(CompositePlainLineParser):

  def __init__(self, subparsers: Optional[Iterable[PlainLineParser]] = None) -> None:
    if not subparsers:
      subparsers = [cls() for cls in DEFAULT_CONSOLE_SUBPARSER_CLASSES]

    super().__init__(subparsers)
