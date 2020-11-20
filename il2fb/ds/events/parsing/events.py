import sys

if sys.version_info >= (3, 9):
  from collections.abc import Container

  Dict = dict

else:
  from typing import Container
  from typing import Dict

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Optional
from typing import TypeVar

from candv import Constants
from candv import VerboseConstant

from il2fb.ds.events.definitions import Event
from il2fb.ds.events.definitions import EventBase

from il2fb.ds.events.definitions.registry import EventRegistry
from il2fb.ds.events.definitions.registry import default_registry

from ._utils import export


class EVT_SRC(Constants):
  CNSL = VerboseConstant("console")
  GLOG = VerboseConstant("gamelog")


ParsingEvent = TypeVar("ParsingEvent")


@export
@dataclass(frozen=True)
class ParsingEvent(EventBase):
  __slots__ = ["evt", "line", "src", ]

  evt:  Optional[Event]
  line: str
  src:  EVT_SRC

  def to_primitive(
    self,
    excludes: Optional[Container[str]] = None,
    *args,
    **kwargs
  ) -> Dict[str, Any]:
    """
    Overrides `to_primitive()` of the parent class.

    """
    evt = self.evt and self.evt.to_primitive(excludes=excludes, *args, **kwargs)

    return dict(
      evt=evt,
      line=self.line,
      src=self.src.name,
    )

  @classmethod
  def from_primitive(
    cls,
    value:    Dict[str, Any],
    registry: Optional[EventRegistry] = None,
    *args,
    **kwargs
  ) -> ParsingEvent:
    """
    Redefines `from_primitive()` of the parent class.

    """
    evt = value['evt']
    if evt:
      registry  = registry or default_registry
      evt_class = registry.get_class_by_name(evt['name'])
      evt = evt_class.from_primitive(evt, *args, **kwargs)

    line = value['line']
    src = EVT_SRC.get(value['src'].upper())

    return cls(
      evt=evt,
      line=line,
      src=src,
    )
