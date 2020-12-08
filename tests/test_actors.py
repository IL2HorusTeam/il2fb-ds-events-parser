import unittest

from il2fb.commons.actors import AIAircraftActor
from il2fb.commons.actors import BridgeActor
from il2fb.commons.actors import BuildingActor
from il2fb.commons.actors import HumanAircraftActor
from il2fb.commons.actors import MovingUnitActor
from il2fb.commons.actors import MovingUnitMemberActor
from il2fb.commons.actors import ObjectActor
from il2fb.commons.actors import StationaryUnitActor

from il2fb.ds.events.parsing.actors import maybe_HumanAircraftActor_from_id
from il2fb.ds.events.parsing.actors import maybe_AIAircraftActor_from_id
from il2fb.ds.events.parsing.actors import maybe_AircraftActor_from_id
from il2fb.ds.events.parsing.actors import maybe_StationaryUnitActor_from_id
from il2fb.ds.events.parsing.actors import maybe_BridgeActor_from_id
from il2fb.ds.events.parsing.actors import maybe_BuildingActor_from_id
from il2fb.ds.events.parsing.actors import maybe_MovingUnitActor_from_id
from il2fb.ds.events.parsing.actors import maybe_MovingUnitMemberActor_from_id
from il2fb.ds.events.parsing.actors import maybe_ObjectActor_from_id
from il2fb.ds.events.parsing.actors import maybe_Actor_from_id
from il2fb.ds.events.parsing.actors import maybe_split_actor_pair

from il2fb.ds.events.parsing.actors import is_tree_id
from il2fb.ds.events.parsing.actors import is_paratrooper_id
from il2fb.ds.events.parsing.actors import is_landscape_id


class MaybeHumanAircraftActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_HumanAircraftActor_from_id("TheUser:P-39D2")

    self.assertEqual(actor.callsign, "TheUser")
    self.assertEqual(actor.aircraft, "P-39D2")

  def test_invalid(self):
    actor = maybe_HumanAircraftActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeAIAircraftActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_AIAircraftActor_from_id("r01200")

    self.assertEqual(actor.id, "r0120")
    self.assertEqual(actor.flight_index, 0)

  def test_invalid(self):
    actor = maybe_AIAircraftActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeAircraftActorFromIdTestCase(unittest.TestCase):

  def test_human_aircraft(self):
    actor = maybe_AircraftActor_from_id("TheUser:P-39D2")
    self.assertIsInstance(actor, HumanAircraftActor)

  def test_ai_aircraft(self):
    actor = maybe_AircraftActor_from_id("r01200")
    self.assertIsInstance(actor, AIAircraftActor)

  def test_invalid(self):
    actor = maybe_AIAircraftActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeMovingUnitActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_MovingUnitActor_from_id("0_Chief")
    self.assertEqual(actor.id, "0_Chief")

  def test_invalid(self):
    actor = maybe_MovingUnitActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeMovingUnitMemberActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_MovingUnitMemberActor_from_id("0_Chief0")
    self.assertEqual(actor.id, "0_Chief")
    self.assertEqual(actor.member_index, 0)

  def test_invalid(self):
    actor = maybe_MovingUnitMemberActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeStationaryUnitActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_StationaryUnitActor_from_id("0_Static")
    self.assertEqual(actor.id, "0_Static")

  def test_invalid(self):
    actor = maybe_StationaryUnitActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeBridgeActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_BridgeActor_from_id("Bridge271")
    self.assertEqual(actor.id, "Bridge271")

  def test_invalid(self):
    actor = maybe_BridgeActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeBuildingActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_BuildingActor_from_id("7071_bld")
    self.assertEqual(actor.id, "7071_bld")

  def test_invalid(self):
    actor = maybe_BuildingActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeObjectActorFromIdTestCase(unittest.TestCase):

  def test_valid(self):
    actor = maybe_ObjectActor_from_id("3do/Buildings/Airdrome/BarrelBlock1/mono.sim")
    self.assertEqual(actor.id, "3do/Buildings/Airdrome/BarrelBlock1/mono.sim")

  def test_invalid(self):
    actor = maybe_ObjectActor_from_id("foo")
    self.assertIsNone(actor)


class MaybeSplitActorPairTestCase(unittest.TestCase):

  def test_pair(self):
    actor1, actor2 = maybe_split_actor_pair("actor 1 and actor 2")
    self.assertEqual(actor1, "actor 1")
    self.assertEqual(actor2, "actor 2")

  def test_single(self):
    actor1, actor2 = maybe_split_actor_pair("actor 1")
    self.assertEqual(actor1, "actor 1")
    self.assertIsNone(actor2)


class MaybeActorFromIdTestCase(unittest.TestCase):

  def test_human_aircraft(self):
    actor = maybe_Actor_from_id("TheUser:P-39D2")
    self.assertIsInstance(actor, HumanAircraftActor)

  def test_ai_aircraft(self):
    actor = maybe_Actor_from_id("r01200")
    self.assertIsInstance(actor, AIAircraftActor)

  def test_stationary_unit(self):
    actor = maybe_Actor_from_id("0_Static")
    self.assertIsInstance(actor, StationaryUnitActor)

  def test_moving_unit(self):
    actor = maybe_Actor_from_id("0_Chief")
    self.assertIsInstance(actor, MovingUnitActor)

  def test_moving_unit_member(self):
    actor = maybe_Actor_from_id("0_Chief0")
    self.assertIsInstance(actor, MovingUnitMemberActor)

  def test_bridge(self):
    actor = maybe_Actor_from_id("Bridge271")
    self.assertIsInstance(actor, BridgeActor)

  def test_building(self):
    actor = maybe_Actor_from_id("7071_bld")
    self.assertIsInstance(actor, BuildingActor)

  def test_object(self):
    actor = maybe_Actor_from_id("3do/Buildings/Airdrome/BarrelBlock1/mono.sim")
    self.assertIsInstance(actor, ObjectActor)

  def test_invalid(self):
    actor = maybe_Actor_from_id("foo")
    self.assertIsNone(actor)


class IsTreeIdTestCase(unittest.TestCase):

  def test_true(self):
    self.assertTrue(is_tree_id("3do/Tree/Line/live.sim"))

  def test_false(self):
    self.assertFalse(is_tree_id("foo"))


class IsParatrooperIdTestCase(unittest.TestCase):

  def test_true(self):
    self.assertTrue(is_paratrooper_id("_para_1"))

  def test_false(self):
    self.assertFalse(is_paratrooper_id("foo"))


class IsLandscapeIdTestCase(unittest.TestCase):

  def test_true(self):
    self.assertTrue(is_landscape_id("landscape"))
    self.assertTrue(is_landscape_id("NONAME"))

  def test_false(self):
    self.assertFalse(is_landscape_id("foo"))
