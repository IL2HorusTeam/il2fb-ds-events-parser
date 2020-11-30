import datetime
import sys

if sys.version_info >= (3, 9):
  Tuple = tuple
else:
  from typing import Tuple

from typing import Union


DATETIME_FMT = "%b %d, %Y %I:%M:%S %p"
TIME_FMT     = "%I:%M:%S %p"

TIMESTAMP_LDELIM = "["
TIMESTAMP_RDELIM = "]"


TimeOrDatetime = Union[datetime.time, datetime.datetime]


def _parse_datetime_or_fail(text: str, fmt: str) -> datetime.datetime:
  return datetime.datetime.strptime(text, fmt)


def parse_datetime_or_fail(text: str) -> datetime.datetime:
  return _parse_datetime_or_fail(text, DATETIME_FMT)


def parse_time_or_fail(text: str) -> datetime.time:
  return _parse_datetime_or_fail(text, TIME_FMT).time()


def split_timestamp_or_fail(text: str) -> Tuple[TimeOrDatetime, str]:
  timestamp, text = text.split(TIMESTAMP_RDELIM, 1)
  timestamp = timestamp.lstrip(TIMESTAMP_LDELIM)

  try:
    timestamp = parse_time_or_fail(timestamp)
  except ValueError:
    timestamp = parse_datetime_or_fail(timestamp)

  text = text.lstrip()

  return (timestamp, text)
