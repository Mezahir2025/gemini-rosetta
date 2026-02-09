import math

class EnemyAI:
    def update_distance(self, player_pos):
        # Modern hardware-accelerated square root
        # No need for bit-level hacking in Python 3.12+
        # We trust the compiler and FPU.
        dx = self.x - player_pos.x
        dy = self.y - player_pos.y
        dist_sq = dx*dx + dy*dy
        distance = math.sqrt(dist_sq)
        
        if distance < 100.0:
            self.state = EnemyState.ATTACK
