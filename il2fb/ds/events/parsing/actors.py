import re

from typing import Optional

from il2fb.commons.actors import AIAircraftActor
from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.actors import MovingUnitActor
from il2fb.commons.actors import MovingUnitMemberActor
from il2fb.commons.actors import StationaryUnitActor

from .literals import HUMAN_AIRCRAFT_DELIM
from .text import strip_spaces


STATIONARY_UNIT_ACTOR_SUFFIX = "_Static"
STATIONARY_UNIT_ACTOR_SUFFIX_LEN = len(STATIONARY_UNIT_ACTOR_SUFFIX)

MOVING_UNIT_ACTOR_SUFFIX     = "_Chief"
MOVING_UNIT_ACTOR_SUFFIX_LEN = len(MOVING_UNIT_ACTOR_SUFFIX)

MOVING_UNIT_MEMBER_ACTOR_REGEX = re.compile(
  rf"(?P<id>\d+){MOVING_UNIT_ACTOR_SUFFIX}(?P<member_index>\d+)"
)


def maybe_HumanAircraftActor_from_id(actor_id: str) -> Optional[HumanAircraftActor]:
  if HUMAN_AIRCRAFT_DELIM in actor_id:
    callsign, aircraft = actor_id.rsplit(HUMAN_AIRCRAFT_DELIM, 1)
    callsign = strip_spaces(callsign)
    return HumanAircraftActor(
      callsign=callsign,
      aircraft=aircraft,
    )


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


def maybe_StationaryUnitActor_from_id(actor_id: str) -> Optional[StationaryUnitActor]:
  if actor_id.endswith(STATIONARY_UNIT_ACTOR_SUFFIX):
    return StationaryUnitActor(
      id=int(actor_id[:-STATIONARY_UNIT_ACTOR_SUFFIX_LEN]),
    )


def maybe_MovingUnitActor_from_id(actor_id: str) -> Optional[MovingUnitActor]:
  if actor_id.endswith(MOVING_UNIT_ACTOR_SUFFIX):
    return MovingUnitActor(
      id=int(actor_id[:-MOVING_UNIT_ACTOR_SUFFIX_LEN]),
    )


def maybe_MovingUnitMemberActor_from_id(actor_id: str) -> Optional[MovingUnitMemberActor]:
  match = MOVING_UNIT_MEMBER_ACTOR_REGEX.match(actor_id)
  if match:
    return MovingUnitMemberActor(
      id=int(match.group('id')),
      member_index=int(match.group('member_index')),
    )
