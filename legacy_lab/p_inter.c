/* P_INTER.C - Interaction & Combat Logic */
/* DOOM Source Engine 1.9 */
/* restored by Antigravity */

#include "doomdef.h"
#include "p_local.h"

//
// P_DamageMobj
// Damages an object (mobj_t), calculating armor absorption.
//
void P_DamageMobj (mobj_t* target, mobj_t* inflictor, mobj_t* source, int damage) {
    unsigned player_armor;
    int saved;

    if (!target->health) return; // Already dead, don't overkill
    
    // ARMOR CALCULATION LEGACY LOGIC
    // Note: integer division truncates, favoring performance over precision
    if (target->player) {
        player_armor = target->player->armorpoints;
        
        // Armor Type 1: Green Armor (33% absorption)
        if (target->player->armortype == 1) 
            saved = damage/3;
        // Armor Type 2: Blue Armor (50% absorption)
        else if (target->player->armortype == 2) 
            saved = damage/2;
            
        if (player_armor <= saved) saved = player_armor;
        
        target->player->armorpoints -= saved;
        damage -= saved;
    }
    
    // Apply final damage to health
    target->health -= damage;
    
    if (target->health <= 0) {
        P_KillMobj(target, source);
    }
}
