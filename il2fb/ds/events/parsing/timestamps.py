import datetime
import sys

if sys.version_info >= (3, 9):
  Tuple = tuple
else:
  from typing import Tuple


DATETIME_FMT = "%b %d, %Y %I:%M:%S %p"
TIME_FMT     = "%I:%M:%S %p"

TIMESTAMP_LDELIM     = "["
TIMESTAMP_LDELIM_LEN = len(TIMESTAMP_LDELIM)
TIMESTAMP_RDELIM     = "] "


def parse_datetime_or_fail(text: str) -> datetime.datetime:
  return datetime.datetime.strptime(text, DATETIME_FMT)


def parse_time_or_fail(text: str) -> datetime.datetime:
  return datetime.datetime.strptime(text, TIME_FMT)


def split_timestamp_or_fail(text: str) -> Tuple[datetime.datetime, str]:
  timestamp, text = text.split(TIMESTAMP_RDELIM, 1)
  timestamp = timestamp[TIMESTAMP_LDELIM_LEN:]

  try:
    timestamp = parse_time_or_fail(timestamp)
  except ValueError:
    timestamp = parse_datetime_or_fail(timestamp)

  return (timestamp, text)
