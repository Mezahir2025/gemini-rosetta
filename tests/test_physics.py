import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from modern_physics import PhysicsObject

class TestPhysicsEngine(unittest.TestCase):
    def setUp(self):
        self.obj = PhysicsObject(x=0, y=0, z=100)

    def test_gravity(self):
        """Test if gravity pulls the object down."""
        self.obj.on_ground = False
        initial_z = self.obj.z
        self.obj.p_z_movement()
        self.assertTrue(self.obj.momz < 0, "Gravity should produce negative vertical momentum")
        self.assertTrue(self.obj.z < initial_z, "Object should fall")

    def test_friction(self):
        """Test if friction slows the object down on X/Y plane."""
        self.obj.momx = 10
        self.obj.on_ground = True
        self.obj.p_xy_movement()
        self.assertTrue(self.obj.momx < 10, "Friction should reduce velocity")
        self.assertTrue(self.obj.momx > 0, "Object should not stop immediately")

    def test_floor_collision(self):
        """Test if object stops when hitting the floor."""
        self.obj.z = 1
        self.obj.momz = -5
        self.obj.on_ground = False
        
        status = self.obj.p_z_movement()
        
        self.assertEqual(self.obj.z, 0, "Object should clamp to floor height")
        self.assertEqual(self.obj.momz, 0, "Momentum should reset on impact")
        self.assertEqual(status, "HIT_FLOOR")

    def test_stopspeed(self):
        """Test if object stops completely below threshold."""
        self.obj.momx = 0.05 # Below STOPSPEED (0.1)
        self.obj.on_ground = True
        self.obj.p_xy_movement()
        self.assertEqual(self.obj.momx, 0, "Object should stop completely")

if __name__ == '__main__':
    unittest.main()
