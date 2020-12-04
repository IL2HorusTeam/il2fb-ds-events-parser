import datetime
import unittest

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionFailedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostLightEvent
from il2fb.ds.events.definitions.connection import HumanConnectionStartedEvent

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLightLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionFailedLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionLostLightLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionLostLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionStartedLineParser


class HumanConnectionStartedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionStartedLineParser()

  def test_parse_line_no_match(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    line = "socket channel '705' start creating: 127.0.0.1:21000"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionStartedEvent)

    self.assertEqual(evt.data.channel_no, 705)
    self.assertEqual(evt.data.address.host, "127.0.0.1")
    self.assertEqual(evt.data.address.port, 21000)


class HumanConnectionFailedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionFailedLineParser()

  def test_parse_line_no_match(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    line = "socket channel NOT created (Timeout.): 127.0.0.1:19841"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionFailedEvent)

    self.assertEqual(evt.data.address.host, "127.0.0.1")
    self.assertEqual(evt.data.address.port, 19841)
    self.assertEqual(evt.data.reason, "Timeout.")

  def test_parse_line_no_reason(self):
    line = "socket channel NOT created (): 127.0.0.1:45292"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionFailedEvent)
    self.assertIsNone(evt.data.reason)


class HumanConnectionEstablishedLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionEstablishedLineParser()

  def test_parse_line_no_match(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    line = "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionEstablishedEvent)

    self.assertEqual(evt.data.channel_no, 699)
    self.assertEqual(evt.data.address.host, "127.0.0.1")
    self.assertEqual(evt.data.address.port, 21000)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_stripped_callsign_spaces(self):
    line = "socket channel '699', ip 127.0.0.1:21000,  The User , is complete created"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionEstablishedEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    line = "socket channel '699', ip 127.0.0.1:21000,  , is complete created"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionEstablishedEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = "socket channel '699', ip 127.0.0.1:21000, , is complete created"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionEstablishedEvent)
    self.assertEqual(evt.data.actor.callsign, "")


class HumanConnectionEstablishedLightLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionEstablishedLightLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser has connected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionEstablishedLightEvent)

    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User  has connected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionEstablishedLightEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "  has connected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionEstablishedLightEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = " has connected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionEstablishedLightEvent)
    self.assertEqual(evt.data.actor.callsign, "")


class HumanConnectionLostLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionLostLineParser()

  def test_parse_line_no_match(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    line = "socketConnection with 127.0.0.1:60500 on channel 709 lost.  Reason: You have been kicked from the server."
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionLostEvent)

    self.assertEqual(evt.data.channel_no, 709)
    self.assertEqual(evt.data.address.host, "127.0.0.1")
    self.assertEqual(evt.data.address.port, 60500)
    self.assertEqual(evt.data.reason, "You have been kicked from the server.")

  def test_parse_line_no_reason(self):
    line = "socketConnection with 127.0.0.1:21000 on channel 703 lost.  Reason: "
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanConnectionLostEvent)
    self.assertIsNone(evt.data.reason)


class HumanConnectionLostLightLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = HumanConnectionLostLightLineParser()

  def test_parse_line_no_match(self):
    timestamp = None
    line = "foo"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsNone(evt)

  def test_parse_line(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = "TheUser has disconnected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionLostLightEvent)

    self.assertEqual(evt.data.timestamp, timestamp)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_stripped_callsign_spaces(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)
    line = " The User  has disconnected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionLostLightEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_empty_callsign(self):
    timestamp = datetime.datetime(2020, 12, 31, 15, 46, 8)

    line = "  has disconnected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionLostLightEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = " has disconnected"
    evt = self.parser.parse_line(timestamp, line)

    self.assertIsInstance(evt, HumanConnectionLostLightEvent)
    self.assertEqual(evt.data.actor.callsign, "")
