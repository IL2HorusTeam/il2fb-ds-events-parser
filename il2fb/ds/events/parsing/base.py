from typing import Optional

from il2fb.ds.events.definitions.base import Event


class SimpleLineParser:

  def parse_line(self, line: str) -> Optional[Event]:
    ...
