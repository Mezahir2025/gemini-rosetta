import random

class InteractionSystem:
    """
    Modern implementation of DOOM's p_inter.c interaction logic.
    Handles damage, armor absorption, and death states.
    """
    
    def __init__(self):
        self.ARMOR_GREEN = 1
        self.ARMOR_BLUE = 2
        
    def calculate_damage(self, target, damage, armor_type, armor_points, is_god_mode=False):
        """
        Calculates final damage after armor absorption and god mode checks.
        Returns (damage_taken, remaining_armor_points)
        """
        if is_god_mode:
            return 0, armor_points
            
        saved = 0
        
        if armor_type == self.ARMOR_GREEN:
            saved = damage // 3
        elif armor_type == self.ARMOR_BLUE:
            saved = damage // 2
            
        if armor_points <= saved:
            saved = armor_points
            armor_points = 0
        else:
            armor_points -= saved
            
        final_damage = damage - saved
        return final_damage, armor_points

    def apply_thrust(self, target, inflictor_pos, damage):
        """
        Calculates momentum/thrust applied by damage.
        """
        if not inflictor_pos:
            return (0, 0)
            
        # Simplified thrust calculation without fixed point math
        mass = getattr(target, 'mass', 100)
        thrust_force = (damage * 1000) / mass
        
        # Simple vector math for direction
        dx = target.x - inflictor_pos[0]
        dy = target.y - inflictor_pos[1]
        length = (dx**2 + dy**2)**0.5
        
        if length == 0:
            return (0,0)
            
        return ((dx/length) * thrust_force, (dy/length) * thrust_force)

    def check_pain_state(self, target, pain_chance):
        """
        Determines if the target should enter pain state.
        """
        return random.randint(0, 255) < pain_chance
