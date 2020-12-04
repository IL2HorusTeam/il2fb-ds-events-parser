import datetime
import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from typing import Optional
from typing import Type

from il2fb.ds.events.definitions.base import Event

from .timestamps import split_timestamp_or_fail

from ._utils import export


@export
class PlainLineParser:

  def parse_line(self, line: str) -> Optional[Event]:
    ...


@export
class CompositePlainLineParser(PlainLineParser):

  def __init__(self, subparsers: Iterable[PlainLineParser]) -> None:
    self._subparsers = tuple(subparsers)

  def parse_line(self, line: str) -> Optional[Event]:
    for subparser in self._subparsers:
      evt = subparser.parse_line(line)
      if evt:
        return evt


class LineWithTimestampParser:

  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[Event]:
    ...


@export
class CompositeLineWithTimestampParser(PlainLineParser):

  def __init__(self, subparsers: Iterable[LineWithTimestampParser]) -> None:
    self._subparsers = tuple(subparsers)

  def parse_line(self, line: str) -> Optional[Event]:
    timestamp, line = split_timestamp_or_fail(line)

    # TODO: check if timestamp is time or datetime

    for subparser in self._subparsers:
      evt = subparser.parse_line(timestamp, line)
      if evt:
        return evt
