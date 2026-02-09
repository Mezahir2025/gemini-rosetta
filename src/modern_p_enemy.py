"""
MODERN_P_ENEMY.PY - AI Logic Bridge (v2026)
------------------------------------------------
Legacy Source: legacy_lab/p_enemy.c (1996)
Modernization: Python 3.12 + NumPy (Optional)
Status: SAFER, READABLE, OPTIMIZED

ARCHAEOLOGIST NOTES:
1. Replaced unsafe pointer arithmetic with Python Class attributes.
2. 'fast inverse square root' (0x5f3759df) is preserved as a historical artifact method,
   but modern math.sqrt() is used for actual production logic due to hardware FP support.
3. Bitwise state flags replaced with IntEnum for readability.
"""

import math
import struct
from enum import IntFlag, auto

# --- 1. MODERN STATE MANAGEMENT (No more magic hex numbers) ---
class EnemyState(IntFlag):
    IDLE = auto()      # 1
    ATTACK = auto()    # 2
    PAIN = auto()      # 4
    INVISIBLE = 127    # Legacy mapping preserved

# --- 2. THE LEGENDARY ALGORITHM (Preserved for History) ---
def q_rsqrt_legacy(number: float) -> float:
    """
    Direct Python port of Quake III's Fast Inverse Square Root.
    WARNING: Not efficient in Python due to struct packing overhead.
    Kept purely for 'Digital Museum' purposes.
    """
    threehalfs = 1.5
    x2 = number * 0.5
    
    # Evil floating point bit level hacking in Python
    # Pack float to bytes, unpack as long (int)
    packed_y = struct.pack('f', number)
    i = struct.unpack('i', packed_y)[0]
    
    i = 0x5f3759df - (i >> 1)  # what the... ?
    
    # Pack int back to bytes, unpack as float
    packed_i = struct.pack('i', i)
    y = struct.unpack('f', packed_i)[0]
    
    y = y * (threehalfs - (x2 * y * y))
    return y

# --- 3. MODERN, SAFE IMPLEMENTATION ---
class EnemyAI:
    def __init__(self, x, y, z, health=100):
        self.x = x
        self.y = y
        self.z = z
        self.health = health
        self.state = EnemyState.IDLE
        self.name = "Boss_Tyrant_T-103"

    def update(self, player_x, player_y):
        """
        Modern update loop.
        Safe from segfaults.
        """
        dx = player_x - self.x
        dy = player_y - self.y
        
        # Modern Distance Calculation (Hardware Optimized)
        dist_sq = dx*dx + dy*dy
        distance = math.sqrt(dist_sq)
        
        # Historical Comparison
        # legacy_inv_dist = q_rsqrt_legacy(dist_sq)
        # legacy_dist = 1.0 / legacy_inv_dist
        
        print(f"[{self.name}] Distance to Target: {distance:.2f} meters")

        # Logic Bridge
        if distance < 100.0:
            print(f"[{self.name}] !!! AGGRO TRIGGERED !!!")
            self.state |= EnemyState.ATTACK

    def debug_status(self):
        print(f"STATUS: Health={self.health} | State={self.state.name} ({self.state.value})")

# --- 4. EXECUTABLE SIMULATION ---
if __name__ == "__main__":
    print("--- INITIATING MODERN AI SIMULATION ---")
    
    # Spawn Entity
    boss = EnemyAI(x=10.0, y=10.0, z=0.0)
    
    # Simulate Player Movement
    player_pos = (50.0, 50.0)
    
    print(f"Player detected at {player_pos}")
    boss.update(*player_pos)
    boss.debug_status()
    
    print("\n--- LEGACY ARTIFACT CHECK ---")
    val = 16.0
    print(f"Modern 1/sqrt({val}) = {1/math.sqrt(val)}")
    try:
        print(f"Legacy Q_rsqrt({val}) = {q_rsqrt_legacy(val)} (Approximation)")
    except Exception as e:
        print(f"Legacy Algorithm Failed in Python Env: {e}")
