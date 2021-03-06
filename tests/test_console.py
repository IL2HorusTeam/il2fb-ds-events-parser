import unittest

from il2fb.ds.events.definitions.chat import ServerChatMessageEvent
from il2fb.ds.events.definitions.chat import SystemChatMessageEvent
from il2fb.ds.events.definitions.chat import HumanChatMessageEvent

from il2fb.ds.events.definitions.cheating import CheatingDetectedEvent

from il2fb.ds.events.definitions.connection import HumanConnectionEstablishedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionFailedEvent
from il2fb.ds.events.definitions.connection import HumanConnectionLostEvent
from il2fb.ds.events.definitions.connection import HumanConnectionStartedEvent

from il2fb.ds.events.parsing.console import ConsoleLineParser

from il2fb.ds.events.parsing.connection import HumanConnectionEstablishedLineParser
from il2fb.ds.events.parsing.connection import HumanConnectionLostLineParser


class ConsoleLineParserTestCase(unittest.TestCase):

  def test_default_subparsers(self):
    parser = ConsoleLineParser()
    items = [
      (ServerChatMessageEvent,          "Chat: Server: \tMessage to everyone"),
      (SystemChatMessageEvent,          "Chat: --- TheUser has left the game."),

      (HumanChatMessageEvent,           "Chat: TheUser: \tMessage to server"),
      (HumanChatMessageEvent,           "Chat:  The User : \tMessage to server"),
      (HumanChatMessageEvent,           "Chat:   : \tMessage to server"),
      (HumanChatMessageEvent,           "Chat: : \tMessage to server"),

      (CheatingDetectedEvent,           "socket channel '203' Cheater was detected! Reason=8: 'Cheat-Engine'"),

      (HumanConnectionEstablishedEvent, "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"),
      (HumanConnectionEstablishedEvent, "socket channel '699', ip 127.0.0.1:21000,  The User , is complete created"),
      (HumanConnectionEstablishedEvent, "socket channel '115', ip 127.0.0.1:4114,   , is complete created"),
      (HumanConnectionEstablishedEvent, "socket channel '115', ip 127.0.0.1:4114, , is complete created"),

      (HumanConnectionFailedEvent,      "socket channel NOT created (): 127.0.0.1:45292"),
      (HumanConnectionFailedEvent,      "socket channel NOT created (Only TREE network structure is supported.): 127.0.0.1:21000"),
      (HumanConnectionFailedEvent,      "socket channel NOT created (Reconnect user): 127.0.0.1:21000"),
      (HumanConnectionFailedEvent,      "socket channel NOT created (Timeout.): 127.0.0.1:19841"),

      (HumanConnectionLostEvent,        "socketConnection with 127.0.0.1:21000 on channel 703 lost.  Reason: "),
      (HumanConnectionStartedEvent,     "socket channel '705' start creating: 127.0.0.1:21000"),
    ]
    for cls, line in items:
      result = parser.parse_line(line)
      self.assertIsInstance(result, cls, msg=f"line={line!r}")

  def test_custom_subparsers(self):
    parser = ConsoleLineParser([
      HumanConnectionEstablishedLineParser(),
    ])

    line = "socket channel '699', ip 127.0.0.1:21000, TheUser, is complete created"
    evt  = parser.parse_line(line)
    self.assertIsInstance(evt, HumanConnectionEstablishedEvent)

    line = "Chat: Server: \tMessage to everyone"
    evt  = parser.parse_line(line)
    self.assertIsNone(evt)
