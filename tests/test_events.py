import unittest

from dataclasses import dataclass

from il2fb.ds.events.definitions import Event
from il2fb.ds.events.definitions.registry import EventRegistry

from il2fb.ds.events.parsing.events import ParsingEvent
from il2fb.ds.events.parsing.events import EVT_SRC


registry = EventRegistry()


@registry.register
@dataclass(frozen=True)
class CustomEvent(Event):
  data: str
  category = "custom"
  verbose_name = "test event"


class ParsingEventTestCase(unittest.TestCase):

  def test_to_primitive_no_evt(self):
    testee = ParsingEvent(
      line="text",
      src=EVT_SRC.CNSL,
      evt=None,
    )
    self.assertEqual(testee.to_primitive(), {
      'line': 'text',
      'src':  'CNSL',
      'evt':  None,
    })

  def test_to_primitive_with_evt(self):
    testee = ParsingEvent(
      line="text",
      src=EVT_SRC.CNSL,
      evt=CustomEvent(data="text"),
    )
    self.assertEqual(testee.to_primitive(), {
      'line': 'text',
      'src':  'CNSL',
      'evt':  {
        'category':     'custom',
        'name':         'CustomEvent',
        'verbose_name': 'test event',
        'help_text':    None,
        'data':         'text',
      },
    })

  def test_from_primitive_no_evt(self):
    testee = ParsingEvent(
      line="text",
      src=EVT_SRC.CNSL,
      evt=None,
    )
    self.assertEqual(testee, ParsingEvent.from_primitive(value={
      'line': 'text',
      'src':  'CNSL',
      'evt':  None,
    }))

  def test_from_primitive_with_evt(self):
    testee = ParsingEvent(
      line="text",
      src=EVT_SRC.CNSL,
      evt=CustomEvent(data="text"),
    )
    self.assertEqual(testee, ParsingEvent.from_primitive(
      registry=registry,
      value={
        'line': 'text',
        'src':  'CNSL',
        'evt':  {
          'category':     'custom',
          'name':         'CustomEvent',
          'verbose_name': 'test event',
          'help_text':    None,
          'data':         'text',
        },
      },
    ))
