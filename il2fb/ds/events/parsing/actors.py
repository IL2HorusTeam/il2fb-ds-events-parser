from typing import Optional

from il2fb.commons.actors import AIAircraftActor


def maybe_AIAircraftActor_from_id(actor_id: str) -> Optional[AIAircraftActor]:
  try:
    return AIAircraftActor(
      regiment_id=actor_id[:-3],
      squadron_id=int(actor_id[-3]),
      flight_id=int(actor_id[-2]),
      flight_index=int(actor_id[-1]),
    )
  except ValueError:
    return
