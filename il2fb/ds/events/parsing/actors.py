from il2fb.commons.actors import AIAircraftActor


def AIAircraftActor_from_id(actor_id: str) -> AIAircraftActor:
  return AIAircraftActor(
    regiment_id=actor_id[:-3],
    squadron_id=int(actor_id[-3]),
    flight_id=int(actor_id[-2]),
    flight_index=int(actor_id[-1]),
  )
