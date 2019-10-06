import time
import unittest

from game.behavior.behavior import CharacterBehavior
from game.player.character import Character
from game.target import Target
from tests.component.test_waypoint_following import FakeController


class TestBehavior(unittest.TestCase):

    def setUp(self):
        self.behavior = CharacterBehavior()

    def test_parsing(self):
        behavior = {'grind': [{'parent': [""], 'key': '1', 'behavior': {}}]}
        self.behavior.resolve_profile(behavior)

        self.assertEqual(len(self.behavior.behavior_trees), 1)

    def test_tick(self):
        behavior_details = {'unit': 'Tick', 'attrs': 'second', 'ops': 'GREATER', 'attr_value': '1', 'actions': 'do nothing'}
        behavior = {'grind': [{'parent': [""], 'key': '1', 'behavior': behavior_details}]}

        self.behavior.resolve_profile(behavior)
        temp = list(self.behavior.interpret('grind', Character(), Target()))
        actions = list(self.behavior.interpret('grind', Character(), Target()))
        time.sleep(1)
        actions_after_sleep = list(self.behavior.interpret('grind', Character(), Target()))

        self.assertEqual(len(actions), 0)
        self.assertEqual(len(actions_after_sleep), 1)

    def test_delay(self):
        behavior_details = {'unit': 'Tick', 'attrs': 'second', 'ops': 'GREATER', 'attr_value': '1', 'actions': 'cast', 'action_value': '1', 'action_duration': '2'}
        behavior = {'grind': [{'parent': [""], 'key': '1', 'behavior': behavior_details}]}

        self.behavior.resolve_profile(behavior)
        for action in self.behavior.interpret('grind', Character(), Target()):
            time_before = time.time()
            action.execute(FakeController())
            time_after = time.time()

        self.assertGreater(time_after - time_before, 2)


