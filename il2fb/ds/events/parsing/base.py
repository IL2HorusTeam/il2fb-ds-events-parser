import sys

if sys.version_info >= (3, 9):
  from collections.abc import Iterable
else:
  from typing import Iterable

from typing import Optional

from il2fb.ds.events.definitions.base import Event


class SimpleLineParser:

  def parse_line(self, line: str) -> Optional[Event]:
    ...


class CompositeLineParser(SimpleLineParser):

  def __init__(self, subparsers: Iterable[SimpleLineParser]) -> None:
    self._subparsers = subparsers

  def parse_line(self, line: str) -> Optional[Event]:
    for subparser in self._subparsers:
      evt = subparser.parse_line(line)
      if evt:
        return evt
