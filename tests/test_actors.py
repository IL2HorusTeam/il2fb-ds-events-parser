import unittest

from il2fb.ds.events.parsing.actors import maybe_AIAircraftActor_from_id


class ActorsTestCase(unittest.TestCase):

  def test_maybe_AIAircraftActor_from_id(self):
    actor = maybe_AIAircraftActor_from_id("r01200")

    self.assertEqual(actor.id, "r0120")
    self.assertEqual(actor.flight_index, 0)

  def test_maybe_AIAircraftActor_from_id_invalid(self):
    actor = maybe_AIAircraftActor_from_id("foo")
    self.assertIsNone(actor)
