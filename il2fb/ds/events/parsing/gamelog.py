import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from typing import Optional

from .base import AbstractLineWithTimestampParser
from .base import CompositeLineWithTimestampParser

from .connection import HumanConnectionEstablishedLightLineParser
from .connection import HumanConnectionLostLightLineParser

from ._utils import export


DEFAULT_GAMELOG_SUBPARSER_CLASSES = (
  HumanConnectionEstablishedLightLineParser,
  HumanConnectionLostLightLineParser,
)


@export
class GamelogLineParser(CompositeLineWithTimestampParser):

  def __init__(self, subparsers: Optional[Iterable[AbstractLineWithTimestampParser]] = None) -> None:
    if not subparsers:
      subparsers = [cls() for cls in DEFAULT_GAMELOG_SUBPARSER_CLASSES]

    super().__init__(subparsers)