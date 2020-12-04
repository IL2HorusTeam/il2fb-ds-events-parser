#!/usr/bin/env python3

import argparse
import contextlib
import operator
import sys
import time

from collections import defaultdict
from collections import OrderedDict as odict

from pathlib import Path

import asciitree

from il2fb.ds.events.parsing.console import DEFAULT_CONSOLE_SUBPARSER_CLASSES


INPUT_STDIN = "-"


def make_args_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="check parsing of console messages from a log file or STDIN",
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


def print_stats(time_elapsed, lines_total, lines_parsed, event_counts, parsers_to_events) -> None:
  event_counts_sorted = sorted(event_counts.items(), key=operator.itemgetter(1), reverse=True)
  lines_parsed_ratio  = (lines_parsed / lines_total) * 100

  max_parser_name_len = max(map(len, parsers_to_events.keys()))
  max_event_name_len = max(map(len, event_counts.keys()))
  max_event_count = max(event_counts.values())
  max_event_count_len = len(str(max_event_count))
  max_event_ratio = "%.4f" % ((max_event_count / lines_parsed) * 100)
  max_event_ratio_len = len(max_event_ratio)
  event_types_count = len(event_counts)
  event_types_count_len = len(str(event_types_count))


  print(f"Time:         {time_elapsed:.6f}s")
  print(f"Lines total:  {lines_total}")
  print(f"Lines parsed: {lines_parsed} ({lines_parsed_ratio:.2f}%)")
  print()
  print("Events frequencies:")
  print()

  line_fmt = f"  %{event_types_count_len}d. %-{max_event_name_len}s %-{max_event_count_len}d / %{max_event_ratio_len}.4f%%"

  for i, (name, count) in enumerate(event_counts_sorted):
    ratio = (count / lines_parsed) * 100
    print(line_fmt % (i + 1, name, count, ratio))

  print()
  print("Parsers frequencies:")
  print()

  parsers_counts = []
  node_name_len  = max(max_parser_name_len, max_event_name_len + 4)

  parser_node_name_fmt = f"%-{node_name_len}s %-{max_event_count_len}d   / %{max_event_ratio_len}.4f%%"
  event_node_name_fmt  = f"%-{node_name_len - 2}s %-{max_event_count_len}d / %{max_event_ratio_len}.4f%%"

  for parser, events in parsers_to_events.items():
    parser_events = []
    parser_count = 0

    for event in events:
      event_count   = event_counts[event]
      event_ratio   = (event_count / lines_parsed) * 100
      parser_count += event_count

      event_node_name = event_node_name_fmt % (event, event_count, event_ratio)
      parser_events.append((event_count, event_node_name))

    parser_events.sort(key=operator.itemgetter(0), reverse=True)
    parser_events = odict([
      (event, dict())
      for _, event in parser_events
    ])

    parser_ratio = (parser_count / lines_parsed) * 100
    parser_node_name = parser_node_name_fmt % (parser, parser_count, parser_ratio)

    parsers_counts.append((parser_count, parser_node_name, parser_events))

  parsers_counts.sort(key=operator.itemgetter(0), reverse=True)
  parsers_counts = odict([
    (parser, parser_events)
    for (_, parser, parser_events) in parsers_counts
  ])
  parsers_counts = odict([
    (f"Total parsed [{lines_parsed}]", parsers_counts)
  ])

  tree_drawer = asciitree.LeftAligned()
  print(tree_drawer(parsers_counts))
  print()



def run(input_stream) -> None:
  parsers = [cls() for cls in DEFAULT_CONSOLE_SUBPARSER_CLASSES]

  lines_total  = 0
  lines_parsed = 0

  event_counts = defaultdict(lambda: 0)
  parsers_to_events = defaultdict(set)

  time_start = time.monotonic()

  for line in input_stream:
    lines_total += 1
    line = line.rstrip()

    for parser in parsers:
      evt = parser.parse_line(line)
      if evt:
        lines_parsed += 1
        event_counts[evt.name] += 1
        parsers_to_events[parser.__class__.__name__].add(evt.name)
        break
    else:
      try:
        sys.stderr.write(f"not parsed: {repr(line)}\n")
      except BrokenPipeError:
        return

  time_elapsed = time.monotonic() - time_start

  print_stats(
    time_elapsed,
    lines_total,
    lines_parsed,
    event_counts,
    parsers_to_events,
  )


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
