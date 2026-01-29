import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from modern_interaction import InteractionSystem

class TestInteractionSystem(unittest.TestCase):
    def setUp(self):
        self.inter = InteractionSystem()
        self.ARMOR_GREEN = 1
        self.ARMOR_BLUE = 2

    def test_no_armor(self):
        """Test damage with no armor."""
        # target=None, damage=50, armor_type=0, armor_points=0
        dmg, armor = self.inter.calculate_damage(None, 50, 0, 0)
        self.assertEqual(dmg, 50)
        self.assertEqual(armor, 0)

    def test_green_armor_absorb(self):
        """Test Green Armor (1/3 absorption)."""
        # 30 damage -> save 10 -> take 20
        dmg, armor = self.inter.calculate_damage(target=None, damage=30, armor_type=self.ARMOR_GREEN, armor_points=100)
        self.assertEqual(dmg, 20)
        self.assertEqual(armor, 90)

    def test_blue_armor_absorb(self):
        """Test Blue Armor (1/2 absorption)."""
        # 30 damage -> save 15 -> take 15
        dmg, armor = self.inter.calculate_damage(target=None, damage=30, armor_type=self.ARMOR_BLUE, armor_points=100)
        self.assertEqual(dmg, 15)
        self.assertEqual(armor, 85)

    def test_armor_depletion(self):
        """Test armor running out."""
        # 30 damage, Green Armor but only 5 points left.
        # Should save 10 normally, but only has 5.
        # So saves 5, takes 25. Armor becomes 0.
        dmg, armor = self.inter.calculate_damage(target=None, damage=30, armor_type=self.ARMOR_GREEN, armor_points=5)
        self.assertEqual(dmg, 25)
        self.assertEqual(armor, 0)

    def test_pain_chance(self):
        """Test pain chance logic (probabilistic)."""
        # This is random, but we check if result is boolean
        result = self.inter.check_pain_state(target=None, pain_chance=128)
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
