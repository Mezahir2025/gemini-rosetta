import math

class PhysicsObject:
    """
    Modern implementation of DOOM's P_MobjThinker physics.
    Replaces fixed-point math with floating point.
    """
    def __init__(self, x=0, y=0, z=0, mass=100):
        self.x = x
        self.y = y
        self.z = z
        self.momx = 0
        self.momy = 0
        self.momz = 0
        
        # Constants from p_mobj.c / doomdef.h
        # FRICTION 0xe800 (approx 0.906 in decimal)
        self.FRICTION = 0.906 
        self.GRAVITY = 1.0  
        self.STOPSPEED = 0.1 # Threshold to stop movement completely

        self.on_ground = True
        self.floor_z = 0
        self.ceiling_z = 1000

    def apply_force(self, fx, fy, fz):
        self.momx += fx
        self.momy += fy
        self.momz += fz

    def p_xy_movement(self):
        """
        Modernized P_XYMovement
        Handies velocity integration and friction.
        """
        # Move
        self.x += self.momx
        self.y += self.momy

        # Apply Friction (Legacy: FixedMul(mom, FRICTION))
        if self.on_ground:
            # Doom stops objects if they are moving very slowly
            if abs(self.momx) < self.STOPSPEED and abs(self.momy) < self.STOPSPEED:
                self.momx = 0
                self.momy = 0
            else:
                self.momx *= self.FRICTION
                self.momy *= self.FRICTION

    def p_z_movement(self):
        """
        Modernized P_ZMovement
        Handles gravity and floor/ceiling collisions.
        """
        # Apply Gravity
        if not self.on_ground:
            self.momz -= self.GRAVITY
        
        # Move
        self.z += self.momz

        # Floor Collision
        if self.z <= self.floor_z:
            self.z = self.floor_z
            self.momz = 0
            self.on_ground = True
            return "HIT_FLOOR" # Return status for sfx logic

        # Ceiling Collision
        if self.z >= self.ceiling_z:
            self.z = self.ceiling_z
            self.momz = 0
            return "HIT_CEILING"
        
        self.on_ground = False
        return "AIRBORNE"

    def tick(self):
        """
        Simulates one gametic.
        """
        self.p_xy_movement()
        return self.p_z_movement()
