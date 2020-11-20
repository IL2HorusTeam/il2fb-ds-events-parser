from typing import Optional
from typing import Union

from il2fb.commons.actors import HumanActor

from il2fb.ds.events.definitions.chat import ChatMessage
from il2fb.ds.events.definitions.chat import HumanChatMessage

from il2fb.ds.events.definitions.chat import ChatMessageEvent
from il2fb.ds.events.definitions.chat import ServerChatMessageEvent
from il2fb.ds.events.definitions.chat import SystemChatMessageEvent
from il2fb.ds.events.definitions.chat import HumanChatMessageEvent


from .base import SimpleLineParser

from ._utils import export


CHAT_PREFIX     = "Chat: "
CHAT_PREFIX_LEN = len(CHAT_PREFIX)

NO_SENDER_PREFIX     = "--- "
NO_SENDER_PREFIX_LEN = len(NO_SENDER_PREFIX)

SENDER_DELIMITER = ": \t"
SENDER_SERVER    = "Server"


@export
class ChatLineParser(SimpleLineParser):
  """
  Parses chat messages.

  Examples of input lines:

    'Chat: --- TheUser has left the game.'
    'Chat: Server: \tMessage to everyone'
    'Chat: TheUser: \tMessage to server'

  """

  def parse_line(self, line: str) -> Optional[ChatMessageEvent]:
    if line.startswith(CHAT_PREFIX):
      line = line[CHAT_PREFIX_LEN:]
      return (
           self._parse_has_no_sender(line)
        or self._parse_has_sender(line)
      )

  @staticmethod
  def _parse_has_no_sender(line: str) -> Optional[SystemChatMessageEvent]:
    if line.startswith(NO_SENDER_PREFIX):
      msg = line[NO_SENDER_PREFIX_LEN:]
      return SystemChatMessageEvent(ChatMessage(
        msg=msg,
      ))

  @staticmethod
  def _parse_has_sender(line: str) -> Optional[Union[ServerChatMessageEvent, HumanChatMessageEvent]]:
    try:
      sender, msg = line.split(SENDER_DELIMITER, 1)
    except ValueError:
      return

    if sender == SENDER_SERVER:
      return ServerChatMessageEvent(ChatMessage(
        msg=msg,
      ))

    else:
      return HumanChatMessageEvent(HumanChatMessage(
        actor=HumanActor(sender),
        msg=msg,
      ))
