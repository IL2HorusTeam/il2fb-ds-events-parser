import abc
import datetime
import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from collections import defaultdict

from typing import Optional
from typing import Type

from il2fb.ds.events.definitions.base import Event

from .timestamps import split_timestamp_or_fail
from .timestamps import TimeOrDatetime

from ._utils import export


@export
class PlainLineParser:

  def parse_line(self, line: str) -> Optional[Event]:
    ...


@export
class CompositePlainLineParser(PlainLineParser):

  def __init__(self, subparsers: Iterable[PlainLineParser]) -> None:
    self._subparsers = subparsers

  def parse_line(self, line: str) -> Optional[Event]:
    for subparser in self._subparsers:
      evt = subparser.parse_line(line)
      if evt:
        return evt


@export
class AbstractLineWithTimestampParser(abc.ABC):

  @property
  @abc.abstractmethod
  def timestamp_class(self) -> Type[TimeOrDatetime]:
    ...

  def parse_line(self, timestamp, line: str) -> Optional[Event]:
    ...


@export
class LineWithDatetimeParser(AbstractLineWithTimestampParser):
  timestamp_class = datetime.datetime


@export
class LineWithTimeParser(AbstractLineWithTimestampParser):
  timestamp_class = datetime.time


@export
class CompositeLineWithTimestampParser(PlainLineParser):

  def __init__(self, subparsers: Iterable[AbstractLineWithTimestampParser]) -> None:
    self._subparsers = defaultdict(list)
    for subparser in subparsers:
      self._subparsers[subparser.timestamp_class].append(subparser)

  def parse_line(self, line: str) -> Optional[Event]:
    timestamp, line = split_timestamp_or_fail(line)

    subparsers = self._subparsers.get(type(timestamp))
    if not subparsers:
      return

    for subparser in subparsers:
      evt = subparser.parse_line(timestamp, line)
      if evt:
        return evt
