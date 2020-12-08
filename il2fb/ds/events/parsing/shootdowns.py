import datetime
import re

from typing import Optional

from il2fb.commons.actors import Actor
from il2fb.commons.actors import AIAircraftActor
from il2fb.commons.actors import BridgeActor
from il2fb.commons.actors import BuildingActor
from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.actors import MovingUnitActor
from il2fb.commons.actors import MovingUnitMemberActor
from il2fb.commons.actors import ObjectActor
from il2fb.commons.actors import StationaryUnitActor

from il2fb.commons.spatial import Point3D

from il2fb.ds.events.definitions.shootdowns import ShotdownEvent

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownSelfEvent

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownSelfEvent

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBridgeEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBridgeInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBuildingEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByBuildingInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitMemberEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByMovingUnitMemberInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByObjectEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByObjectInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByStationaryUnitEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByStationaryUnitInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByTreeEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByTreeInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByParatrooperEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByParatrooperInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBridgeEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBridgeInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBuildingEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByBuildingInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitMemberEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByMovingUnitMemberInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByObjectEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByObjectInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByStationaryUnitEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByStationaryUnitInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByTreeEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByTreeInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByParatrooperEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByParatrooperInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByAIAircraftAndHumanAircraftInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import AIAircraftShotdownByHumanAircraftAndHumanAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByAIAircraftAndHumanAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndAIAircraftInfo

from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent
from il2fb.ds.events.definitions.shootdowns import HumanAircraftShotdownByHumanAircraftAndHumanAircraftInfo

from .actors import is_landscape_id
from .actors import is_paratrooper_id
from .actors import is_tree_id
from .actors import maybe_Actor_from_id
from .actors import maybe_AircraftActor_from_id
from .actors import maybe_split_actor_pair

from .base import LineWithTimestampParser

from .regex import TARGET_REGEX
from .regex import ATTACKER_REGEX
from .regex import POS_REGEX

from ._utils import export


ACTOR_SHOT_DOWN_REGEX = re.compile(
  rf"^{TARGET_REGEX} shot down by {ATTACKER_REGEX} at {POS_REGEX}$"
)


@export
class ActorShotdownLineParser(LineWithTimestampParser):
  """
  Parses gamelog messages about shootdowns.

  Examples of input lines:

    "r01001 shot down by  at 145663.6 62799.64"
    "r01001 shot down by  at 145663.6 62799.64 83.96088"

    "r01001 shot down by landscape at 145663.6 62799.64"
    "r01001 shot down by landscape at 145663.6 62799.64 83.96088"
    "r01001 shot down by NONAME at 145663.6 62799.64"
    "r01001 shot down by NONAME at 145663.6 62799.64 83.96088"

    "r01001 shot down by g01002 at 145663.6 62799.64"
    "r01001 shot down by g01002 at 145663.6 62799.64 83.96088"

    "r01001 shot down by  Bridge159 at 145663.6 62799.64"
    "r01001 shot down by  Bridge159 at 145663.6 62799.64 83.96088"

    "r01001 shot down by 194_bld at 145663.6 62799.64"
    "r01001 shot down by 194_bld at 145663.6 62799.64 83.96088"

    "r01001 shot down by 0_Chief at 145663.6 62799.64"
    "r01001 shot down by 0_Chief at 145663.6 62799.64 83.96088"

    "r01001 shot down by 0_Chief0 at 145663.6 62799.64"
    "r01001 shot down by 0_Chief0 at 145663.6 62799.64 83.96088"

    "r01001 shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64"
    "r01001 shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"

    "r01001 shot down by _para_1 at 145663.6 62799.64"
    "r01001 shot down by _para_1 at 145663.6 62799.64 83.96088"

    "r01001 shot down by 1240_Static at 145663.6 62799.64"
    "r01001 shot down by 1240_Static at 145663.6 62799.64 83.96088"

    "r01001 shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64"
    "r01001 shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"

    "r01001 shot down by TheUser:TB-7_M40F at 145663.6 62799.64"
    "r01001 shot down by TheUser:TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by  The User :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by :TB-7_M40F at 145663.6 62799.64 83.96088"

    "r01001 shot down by g01002 and g01003 at 145663.6 62799.64"
    "r01001 shot down by g01002 and g01003 at 145663.6 62799.64 83.96088"

    "r01001 shot down by g01002 and TheUser:TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by g01002 and TheUser:TB-7_M40F at 145663.6 62799.64"
    "r01001 shot down by g01002 and  The User :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by g01002 and  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by g01002 and :TB-7_M40F at 145663.6 62799.64 83.96088"

    "r01001 shot down by TheUser:TB-7_M40F and g01002 at 145663.6 62799.64"
    "r01001 shot down by TheUser:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "r01001 shot down by  The User :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "r01001 shot down by  :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "r01001 shot down by :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"

    "r01001 shot down by TheUser:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64"
    "r01001 shot down by TheUser:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by  The User :TB-7_M40F and  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by  :TB-7_M40F and  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "r01001 shot down by :TB-7_M40F and :TB-7_M40F at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by  at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by  at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by landscape at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by landscape at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by NONAME at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by NONAME at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by g01002 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by g01002 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by  Bridge159 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 194_bld at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 194_bld at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 0_Chief at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 0_Chief at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 0_Chief0 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 3do/Buildings/Airdrome/BarrelBlock1/mono.sim at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by _para_1 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by _para_1 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 1240_Static at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 1240_Static at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"
    " The User :TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"
    " :TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"
    ":TB-7_M40F shot down by 3do/Tree/Line/live.sim at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by :TB-7_M40F at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by g01002 and g01003 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by g01002 and g01003 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by g01002 and TheUser2:TB-7_M40F at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by g01002 and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by g01002 and  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by g01002 and  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by g01002 and :TB-7_M40F at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and g01002 at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  The User :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by :TB-7_M40F and g01002 at 145663.6 62799.64 83.96088"

    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64"
    "TheUser:TB-7_M40F shot down by TheUser2:TB-7_M40F and TheUser2:TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  The User :TB-7_M40F and  The User2 :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by  :TB-7_M40F and  :TB-7_M40F at 145663.6 62799.64 83.96088"
    "TheUser:TB-7_M40F shot down by :TB-7_M40F and :TB-7_M40F at 145663.6 62799.64 83.96088"

  """
  def parse_line(self, timestamp: datetime.datetime, line: str) -> Optional[ShotdownEvent]:
    match = ACTOR_SHOT_DOWN_REGEX.match(line)
    if not match:
      return

    pos = Point3D(
      x=float(match.group('x')),
      y=float(match.group('y')),
      z=float(match.group('z') or 0),
    )

    target_id = match.group('target')
    target    = maybe_AircraftActor_from_id(target_id)

    if not target:
      return

    attacker       = None
    assistant      = None
    is_tree        = False
    is_landscape   = False
    is_paratrooper = False

    attacker_id = match.group('attacker')

    if attacker_id:
      attacker_id, assistant_id = maybe_split_actor_pair(attacker_id)
      if assistant_id:    # check if "by pair"
        assistant = maybe_AircraftActor_from_id(assistant_id)
        attacker  = maybe_AircraftActor_from_id(attacker_id)
        if not attacker:  # failed to parse assistant, switch from "by pair" to "by single"
          attacker, assistant = assistant, None
      else:
        is_landscape = is_landscape_id(attacker_id)
        if not is_landscape:
          is_tree = is_tree_id(attacker_id)
          if not is_tree:
            is_paratrooper = is_paratrooper_id(attacker_id)
            if not is_paratrooper:
              attacker = maybe_Actor_from_id(attacker_id)

    target_type    = type(target)
    attacker_type  = type(attacker)
    assistant_type = type(assistant)

    if is_landscape:
      if target_type is HumanAircraftActor:
        return HumanAircraftShotdownSelfEvent(HumanAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
      elif target_type is AIAircraftActor:
        return AIAircraftShotdownSelfEvent(AIAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
    elif is_tree:
      if target_type is HumanAircraftActor:
        return HumanAircraftShotdownByTreeEvent(HumanAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
      elif target_type is AIAircraftActor:
        return AIAircraftShotdownByTreeEvent(AIAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
    elif is_paratrooper:
      if target_type is HumanAircraftActor:
        return HumanAircraftShotdownByParatrooperEvent(HumanAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
      elif target_type is AIAircraftActor:
        return AIAircraftShotdownByParatrooperEvent(AIAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
    elif not attacker:
      if target_type is HumanAircraftActor:
        return HumanAircraftShotdownEvent(HumanAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
      elif target_type is AIAircraftActor:
        return AIAircraftShotdownEvent(AIAircraftShotdownInfo(
          timestamp=timestamp,
          pos=pos,
          target=target,
        ))
    elif assistant:
      if target_type is HumanAircraftActor:
        if attacker_type is HumanAircraftActor:
          if assistant_type is HumanAircraftActor:
            return HumanAircraftShotdownByHumanAircraftAndHumanAircraftEvent(
              HumanAircraftShotdownByHumanAircraftAndHumanAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
          elif assistant_type is AIAircraftActor:
            return HumanAircraftShotdownByHumanAircraftAndAIAircraftEvent(
              HumanAircraftShotdownByHumanAircraftAndAIAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
        elif attacker_type is AIAircraftActor:
          if assistant_type is HumanAircraftActor:
            return HumanAircraftShotdownByAIAircraftAndHumanAircraftEvent(
              HumanAircraftShotdownByAIAircraftAndHumanAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
          elif assistant_type is AIAircraftActor:
            return HumanAircraftShotdownByAIAircraftAndAIAircraftEvent(
              HumanAircraftShotdownByAIAircraftAndAIAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
      elif target_type is AIAircraftActor:
        if attacker_type is HumanAircraftActor:
          if assistant_type is HumanAircraftActor:
            return AIAircraftShotdownByHumanAircraftAndHumanAircraftEvent(
              AIAircraftShotdownByHumanAircraftAndHumanAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
          elif assistant_type is AIAircraftActor:
            return AIAircraftShotdownByHumanAircraftAndAIAircraftEvent(
              AIAircraftShotdownByHumanAircraftAndAIAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
        elif attacker_type is AIAircraftActor:
          if assistant_type is HumanAircraftActor:
            return AIAircraftShotdownByAIAircraftAndHumanAircraftEvent(
              AIAircraftShotdownByAIAircraftAndHumanAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
          elif assistant_type is AIAircraftActor:
            return AIAircraftShotdownByAIAircraftAndAIAircraftEvent(
              AIAircraftShotdownByAIAircraftAndAIAircraftInfo(
                timestamp=timestamp,
                pos=pos,
                target=target,
                attacker=attacker,
                assistant=assistant,
              ),
            )
    else:
      if target_type is HumanAircraftActor:
        if attacker_type is HumanAircraftActor:
          return HumanAircraftShotdownByHumanAircraftEvent(
            HumanAircraftShotdownByHumanAircraftInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is AIAircraftActor:
          return HumanAircraftShotdownByAIAircraftEvent(
            HumanAircraftShotdownByAIAircraftInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is StationaryUnitActor:
          return HumanAircraftShotdownByStationaryUnitEvent(
            HumanAircraftShotdownByStationaryUnitInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is MovingUnitActor:
          return HumanAircraftShotdownByMovingUnitEvent(
            HumanAircraftShotdownByMovingUnitInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is MovingUnitMemberActor:
          return HumanAircraftShotdownByMovingUnitMemberEvent(
            HumanAircraftShotdownByMovingUnitMemberInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is BridgeActor:
          return HumanAircraftShotdownByBridgeEvent(
            HumanAircraftShotdownByBridgeInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is BuildingActor:
          return HumanAircraftShotdownByBuildingEvent(
            HumanAircraftShotdownByBuildingInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is ObjectActor:
          return HumanAircraftShotdownByObjectEvent(
            HumanAircraftShotdownByObjectInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
      elif target_type is AIAircraftActor:
        if attacker_type is HumanAircraftActor:
          return AIAircraftShotdownByHumanAircraftEvent(
            AIAircraftShotdownByHumanAircraftInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is AIAircraftActor:
          return AIAircraftShotdownByAIAircraftEvent(
            AIAircraftShotdownByAIAircraftInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is StationaryUnitActor:
          return AIAircraftShotdownByStationaryUnitEvent(
            AIAircraftShotdownByStationaryUnitInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is MovingUnitActor:
          return AIAircraftShotdownByMovingUnitEvent(
            AIAircraftShotdownByMovingUnitInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is MovingUnitMemberActor:
          return AIAircraftShotdownByMovingUnitMemberEvent(
            AIAircraftShotdownByMovingUnitMemberInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is BridgeActor:
          return AIAircraftShotdownByBridgeEvent(
            AIAircraftShotdownByBridgeInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is BuildingActor:
          return AIAircraftShotdownByBuildingEvent(
            AIAircraftShotdownByBuildingInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
        elif attacker_type is ObjectActor:
          return AIAircraftShotdownByObjectEvent(
            AIAircraftShotdownByObjectInfo(
              timestamp=timestamp,
              pos=pos,
              target=target,
              attacker=attacker,
            ),
          )
