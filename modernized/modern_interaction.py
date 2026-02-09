class DamageSystem:
    def calculate_damage(self, target, damage, armor_type):
        # Strategy Pattern for Armor Absorption
        # Clean, readable logic replacing spaghetti if-else
        if armor_type == ArmorType.GREEN:
            saved = damage // 3
        elif armor_type == ArmorType.BLUE:
            saved = damage // 2
        else:
            saved = 0
            
        # Ensure we don't heal the player by accident (Sanity Check)
        final_damage = max(0, damage - saved)
        target.take_damage(final_damage)
