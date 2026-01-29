
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from modern_ai_prototype import Monster, NodeStatus

class TestModernAI(unittest.TestCase):
    def setUp(self):
        self.monster = Monster("Cacodemon")

    def test_idle_pattern(self):
        print("\n--- TEST: Idle Pattern ---")
        # Default state should be Idle
        status = self.monster.update()
        self.assertEqual(status, NodeStatus.SUCCESS)
        self.assertFalse(self.monster.target_acquired)

    def test_sighted_player(self):
        print("\n--- TEST: Sighted Player ---")
        self.monster.can_see_player = True
        # First tick initializes chase
        status = self.monster.update()
        self.assertTrue(self.monster.target_acquired)
        # Should start moving because dist is 100
        self.monster.movecount = 2
        status = self.monster.update()
        self.assertEqual(status, NodeStatus.RUNNING)

    def test_heard_noise(self):
        print("\n--- TEST: Heard Noise ---")
        self.monster.has_heard_sound = True
        status = self.monster.update()
        self.assertTrue(self.monster.target_acquired)
        self.assertEqual(self.monster.name, "Cacodemon")

    def test_lost_player(self):
        print("\n--- TEST: Lost Player (Reset to Idle) ---")
        self.monster.can_see_player = True
        self.monster.update() # Target acquired
        
        # Player disappears
        self.monster.can_see_player = False
        self.monster.has_heard_sound = False
        status = self.monster.update()
        # Should fall back to ActionIdle
        self.assertEqual(status, NodeStatus.SUCCESS)

    def test_attack_transition(self):
        print("\n--- TEST: Attack Transition ---")
        self.monster.can_see_player = True
        self.monster.dist_to_player = 10 # Very close
        self.monster.update()
        # Check logs/logic - distance < 50 triggers Attack
        # The logic in prototype is: if dist < 50, perform attack node which returns success
        status = self.monster.update()
        self.assertEqual(status, NodeStatus.SUCCESS)

if __name__ == "__main__":
    unittest.main()
