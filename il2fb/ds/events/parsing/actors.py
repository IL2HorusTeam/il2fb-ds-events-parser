import re
import sys

if sys.version_info >= (3, 9):
  Tuple = tuple
else:
  from typing import Tuple

from typing import Optional
from typing import Union

from il2fb.commons.actors import Actor
from il2fb.commons.actors import AIAircraftActor
from il2fb.commons.actors import BridgeActor
from il2fb.commons.actors import BuildingActor
from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.actors import MovingUnitActor
from il2fb.commons.actors import MovingUnitMemberActor
from il2fb.commons.actors import ObjectActor
from il2fb.commons.actors import StationaryUnitActor

from .literals import HUMAN_AIRCRAFT_DELIM
from .text import strip_spaces

from .regex import ATTACKER_REGEX
from .regex import ASSISTANT_REGEX


BRIDGE_ACTOR_PREFIX          = "Bridge"
BUILDING_ACTOR_SUFFIX        = "_bld"
MOVING_UNIT_ACTOR_SUFFIX     = "_Chief"
OBJECT_ACTOR_PREFIX          = "3do/"
TREE_ACTOR_PREFIX            = "3do/Tree/"
PARATROOPER_ACTOR_PREFIX     = "_para_"
STATIONARY_UNIT_ACTOR_SUFFIX = "_Static"

LANDSCAPE_IDS = {
  'landscape',
  'NONAME',
}


MOVING_UNIT_MEMBER_ACTOR_REGEX = re.compile(
  rf"(?P<id>\d+{MOVING_UNIT_ACTOR_SUFFIX})(?P<member_index>\d+)",
)

ATTACKER_PAIR_REGEX = re.compile(
  rf"^{ATTACKER_REGEX} and {ASSISTANT_REGEX}$",
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
      id=actor_id[:-1],
      flight_index=int(actor_id[-1]),
    )
  except ValueError:
    return


def maybe_AircraftActor_from_id(actor_id: str) -> Optional[Union[
  HumanAircraftActor,
  AIAircraftActor,
]]:
  return (
       maybe_HumanAircraftActor_from_id(actor_id)
    or maybe_AIAircraftActor_from_id(actor_id)
  )


def maybe_MovingUnitActor_from_id(actor_id: str) -> Optional[MovingUnitActor]:
  if actor_id.endswith(MOVING_UNIT_ACTOR_SUFFIX):
    return MovingUnitActor(id=actor_id)


def maybe_MovingUnitMemberActor_from_id(actor_id: str) -> Optional[MovingUnitMemberActor]:
  match = MOVING_UNIT_MEMBER_ACTOR_REGEX.match(actor_id)
  if match:
    return MovingUnitMemberActor(
      id=match.group('id'),
      member_index=int(match.group('member_index')),
    )


def maybe_StationaryUnitActor_from_id(actor_id: str) -> Optional[StationaryUnitActor]:
  if actor_id.endswith(STATIONARY_UNIT_ACTOR_SUFFIX):
    return StationaryUnitActor(id=actor_id)


def maybe_BridgeActor_from_id(actor_id: str) -> Optional[MovingUnitActor]:
  if actor_id.startswith(BRIDGE_ACTOR_PREFIX):
    return BridgeActor(id=actor_id)


def maybe_BuildingActor_from_id(actor_id: str) -> Optional[MovingUnitActor]:
  if actor_id.endswith(BUILDING_ACTOR_SUFFIX):
    return BuildingActor(id=actor_id)


def maybe_ObjectActor_from_id(actor_id: str) -> Optional[ObjectActor]:
  if actor_id.startswith(OBJECT_ACTOR_PREFIX):
    return ObjectActor(id=actor_id)


def maybe_split_actor_pair(actor_id: str) -> Tuple[str, Optional[str]]:
  match = ATTACKER_PAIR_REGEX.match(actor_id)
  if match:
    return (match.group('attacker'), match.group('assistant'))
  else:
    return (actor_id, None)


def maybe_Actor_from_id(actor_id: str) -> Optional[Actor]:
  if (actor := maybe_HumanAircraftActor_from_id(actor_id)):
    return actor

  actor_id = actor_id.strip()

  return (
       maybe_StationaryUnitActor_from_id(actor_id)

    or maybe_MovingUnitActor_from_id(actor_id)
    or maybe_MovingUnitMemberActor_from_id(actor_id)
    or maybe_BridgeActor_from_id(actor_id)
    or maybe_BuildingActor_from_id(actor_id)
    or maybe_ObjectActor_from_id(actor_id)

    # AIAircraftActor should be the last, as it does not have a constant
    # prefix or suffix
    or maybe_AIAircraftActor_from_id(actor_id)
  )


def is_tree_id(actor_id: str) -> bool:
  return actor_id.startswith(TREE_ACTOR_PREFIX)


def is_paratrooper_id(actor_id: str) -> bool:
  return actor_id.startswith(PARATROOPER_ACTOR_PREFIX)


def is_landscape_id(actor_id: str) -> bool:
  return actor_id in LANDSCAPE_IDS
