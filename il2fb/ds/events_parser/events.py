import sys

from dataclasses import dataclass
from dataclasses import field

if sys.version_info < (3, 9):
  from typing import Container
else:
  from collections.abc import Container

from typing import Any
from typing import Dict
from typing import Optional
from typing import TypeVar

from candv import Constants
from candv import VerboseConstant

from il2fb.ds.events import Event
from il2fb.ds.events import EventBase
from il2fb.ds.events import registry

from .utils import export


class EVT_SRC(Constants):
  CNSL = VerboseConstant("console")
  GLOG = VerboseConstant("gamelog")


ParsedEvent = TypeVar("ParsedEvent")


@export
@dataclass(frozen=True)
class ParsedEvent(EventBase):
  evt:  Optional[Event]
  line: str
  src:  EVT_SRC

  def to_primitive(self, excludes: Optional[Container[str]] = None) -> Dict[str, Any]:
    """
    Redefines `to_primitive()` of the parent class.

    """
    evt = self.evt.to_primitive(excludes=excludes) if self.evt else None

    return dict(
      evt=evt,
      line=self.line,
      src=self.src.name,
    )

  @classmethod
  def from_primitive(cls, value: Dict[str, Any]) -> ParsedEvent:
    """
    Redefines `from_primitive()` of the parent class.

    """
    evt = value['value']
    if evt:
      evt_class = registry.get_class_by_name(evt['name'])
      evt = evt_class.from_primitive(evt)

    line = value['line']
    src = EVT_SRC.get(value['src'])

    return cls(
      evt=evt,
      line=line,
      src=src,
    )
