import unittest

from il2fb.ds.events.definitions.chat import ServerChatMessageEvent
from il2fb.ds.events.definitions.chat import SystemChatMessageEvent
from il2fb.ds.events.definitions.chat import HumanChatMessageEvent

from il2fb.ds.events.parsing.chat import ChatLineParser


class ChatLineParserTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = ChatLineParser()

  def test_parse_line_not_chat_message(self):
    line = "foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line_invalid_message(self):
    line = "Chat: foo"
    evt  = self.parser.parse_line(line)

    self.assertIsNone(evt)

  def test_parse_line_system_message(self):
    line = "Chat: --- TheUser has left the game."
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, SystemChatMessageEvent)
    self.assertEqual(evt.data.msg, "TheUser has left the game.")

  def test_parse_line_server_message(self):
    line = "Chat: Server: \tMessage to everyone"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, ServerChatMessageEvent)
    self.assertEqual(evt.data.msg, "Message to everyone")

  def test_parse_line_human_message(self):
    line = "Chat: TheUser: \tMessage to server"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanChatMessageEvent)
    self.assertEqual(evt.data.msg, "Message to server")
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_human_message_stripped_callsign_spaces(self):
    line = "Chat:  The User : \tMessage to server"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanChatMessageEvent)
    self.assertEqual(evt.data.actor.callsign, "TheUser")

  def test_parse_line_human_message_empty_callsign(self):
    line = "Chat:  : \tMessage to server"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanChatMessageEvent)
    self.assertEqual(evt.data.actor.callsign, "")

    line = "Chat: : \tMessage to server"
    evt  = self.parser.parse_line(line)

    self.assertIsInstance(evt, HumanChatMessageEvent)
    self.assertEqual(evt.data.actor.callsign, "")
