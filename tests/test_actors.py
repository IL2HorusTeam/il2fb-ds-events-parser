import unittest

from il2fb.ds.events.parsing.actors import AIAircraftActor_from_id


class ActorsTestCase(unittest.TestCase):

  def test_AIAircraftActor_from_id(self):
    actor = AIAircraftActor_from_id("r01200")

    self.assertEqual(actor.regiment_id,  "r01")
    self.assertEqual(actor.squadron_id,  2)
    self.assertEqual(actor.flight_id,    0)
    self.assertEqual(actor.flight_index, 0)
