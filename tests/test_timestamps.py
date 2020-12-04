import datetime
import unittest

from il2fb.ds.events.parsing.timestamps import parse_datetime_or_fail
from il2fb.ds.events.parsing.timestamps import parse_time_or_fail
from il2fb.ds.events.parsing.timestamps import split_timestamp_or_fail


class ParseDatetimeOrFailTestCase(unittest.TestCase):

  def test_valid(self):
    timestamp = parse_datetime_or_fail("Aug 3, 2020 3:46:08 PM")
    self.assertEqual(timestamp, datetime.datetime(2020, 8, 3, 15, 46, 8))

  def test_invalid(self):
    with self.assertRaises(ValueError):
      parse_datetime_or_fail("foo")


class ParseTimeOrFailTestCase(unittest.TestCase):

  def test_valid(self):
    timestamp = parse_time_or_fail("3:46:16 PM")
    self.assertEqual(timestamp, datetime.datetime(1900, 1, 1, 15, 46, 16))

  def test_invalid(self):
    with self.assertRaises(ValueError):
      parse_time_or_fail("foo")


class SplitTimestampOrFailTestCase(unittest.TestCase):

  def test_datetime(self):
    line = "[Aug 3, 2020 3:46:08 PM] foo"
    timestamp, line = split_timestamp_or_fail(line)
    self.assertEqual(timestamp, datetime.datetime(2020, 8, 3, 15, 46, 8))
    self.assertEqual(line, "foo")

  def test_time(self):
    line = "[3:46:16 PM] foo"
    timestamp, line = split_timestamp_or_fail(line)
    self.assertEqual(timestamp, datetime.datetime(1900, 1, 1, 15, 46, 16))
    self.assertEqual(line, "foo")

  def test_left_spaces_preserved(self):
    line = "[3:46:16 PM]      foo"
    timestamp, line = split_timestamp_or_fail(line)
    self.assertEqual(timestamp, datetime.datetime(1900, 1, 1, 15, 46, 16))
    self.assertEqual(line, "     foo")


  def test_invalid_timestamp(self):
    with self.assertRaises(ValueError):
      parse_time_or_fail("[foo] bar")

  def test_invalid_line(self):
    with self.assertRaises(ValueError):
      parse_time_or_fail("foo")
