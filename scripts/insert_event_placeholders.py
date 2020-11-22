#!/usr/bin/env python3

import argparse
import itertools
import re

from pathlib import Path


def make_args_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="substitute generic tokens with placeholders in a log file or STDIN",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument(
    dest="input",
    type=str,
    help=f"path to a log file",
  )
  parser.add_argument(
    dest="callsigns_file_path",
    type=str,
    help=f"path to a file with callsigns",
  )
  parser.add_argument(
    dest="wings_file_path",
    nargs="?",
    type=str,
    help=f"path to a file with AI wings",
  )
  return parser


def run(input_stream, callsigns=None, wings=None) -> None:
  transformers = [
    (
      re.compile(r"^\[\d+:\d+:\d+ [AP]M\]"),
      "__time__",
    ),
    (
      re.compile(r"^\[\w+ \d+, \d+ \d+:\d+:\d+ [AP]M\]"),
      "__date__",
    ),
    (
      re.compile(r"at (-?\d+\.\d+ )+-?\d+\.\d+"),
      "__coord__",
    ),
    (
      re.compile(r"\b\d+_Static\b"),
      "__static__",
    ),
    (
      re.compile(r"\b\d+_Chief\d+\b"),
      "__chief_member__",
    ),
    (
      re.compile(r"\b\d+_Chief\b"),
      "__chief__",
    ),
    (
      re.compile(r"\bBridge\d+(\w+\d+)?\b"),
      "__bridge__",
    ),
    (
      re.compile(r"\b\d+_bld\b"),
      "__bld__",
    ),
    (
      re.compile(r"\b[Nn](.+/)+.+\.mis\b"),
      "__mis__",
    ),
    (
      re.compile(r"\b3do/(.+/)+.+\.sim\b"),
      "__3do__",
    ),
    (
      re.compile(r"fuel \d+%"),
      "__fuel%__",
    ),
    (
      re.compile(r"weapons '.+'"),
      "__weapons__",
    ),
    (
      re.compile(r"army .+\b"),
      "__army__",
    ),
    (
      re.compile(r" engine\(\d+\) "),
      " __engine_N__ ",
    ),
    (
      re.compile(r" fuel tank\(\d+\) "),
      " __fuel_tank_N__ ",
    ),
    (
      re.compile(r" oil radiator\(\d+\) "),
      " __oil_radiator_N__ ",
    ),
  ]

  if wings:
    transformers.extend(list(itertools.chain(*[
      [
        (
          re.compile(rf" {wing}\d\(-1\) "),
          " __ai_paratrooper__ ",
        ),
        (
          re.compile(rf" {wing}\d\(\d+\) "),
          " __ai_aircraft_member__ ",
        ),
        (
          re.compile(rf" {wing}\d "),
          " __ai_aircraft__ ",
        ),
      ]
      for wing in map(re.escape, wings)
    ])))

  if callsigns:
    transformers.extend(list(itertools.chain(*[
      [
        (
          re.compile(rf" {callsign}:[a-zA-z0-9-_./]+\(-1\) "),
          " __human_paratrooper__ ",
        ),
        (
          re.compile(rf" {callsign}:[a-zA-z0-9-_./]+\(\d+\) "),
          " __human_aircraft_member__ ",
        ),
        (
          re.compile(rf" {callsign}:[a-zA-z0-9-_./]+ "),
          " __human_aircraft__ ",
        ),
        (
          re.compile(rf" {callsign} "),
          " __human__ ",
        ),
      ]
      for callsign in map(re.escape, callsigns)
    ])))

  transformers.extend([
    (
      re.compile(r"\s+"),
      " ",
    ),
  ])

  for line in input_stream:
    line = line.strip()
    if not line:
      continue

    for regex, placeholder in transformers:
      line = regex.sub(placeholder, line)

    try:
      print(line)
    except BrokenPipeError:
      return


def main() -> None:
  args_parser = make_args_parser()
  args = args_parser.parse_args()

  callsigns = (
    Path(args.callsigns_file_path).read_text().splitlines()
    if args.callsigns_file_path
    else None
  )

  wings = (
    Path(args.wings_file_path).read_text().splitlines()
    if args.wings_file_path
    else None
  )

  with open(args.input, "rt") as input_stream:
    run(input_stream, callsigns, wings)


if __name__ == "__main__":
  main()
