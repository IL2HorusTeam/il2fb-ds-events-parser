#!/usr/bin/env python3

import argparse
import contextlib

from pathlib import Path

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionLostLightLineParser


INPUT_STDIN = "-"


def make_args_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="extract callsigns of users from a log file or STDIN",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument(
    dest="input",
    nargs="?",
    default=INPUT_STDIN,
    type=str,
    help=f"path to an input file or '{INPUT_STDIN}' for STDIN",
  )
  return parser


def run(input_stream) -> None:
  parsers = [
    HumanConnectionEstablishedLightLineParser(),
    HumanConnectionLostLightLineParser(),
  ]
  callsigns = set()

  for line in input_stream:
    line = line.strip()
    if not line:
      continue

    for parser in parsers:
      evt = parser.parse_line(line)
      if evt:
        callsigns.add(evt.data.actor.callsign)

  if not callsigns:
    raise ValueError("no callsigs collected")

  for callsign in sorted(callsigns):
    print(callsign)


def main() -> None:
  args_parser = make_args_parser()
  args = args_parser.parse_args()

  input_stream_manager = (
    contextlib.nullcontext(enter_result=sys.stdin)
    if args.input == INPUT_STDIN
    else contextlib.closing(open(args.input, "rt"))
  )
  with input_stream_manager as input_stream:
    run(input_stream)


if __name__ == "__main__":
  main()
