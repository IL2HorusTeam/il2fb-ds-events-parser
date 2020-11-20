import datetime


TIME_FMT = "%I:%M:%S %p"


def parse_time_or_fail(text: str) -> datetime.time:
  return datetime.datetime.strptime(text, TIME_FMT).time()
