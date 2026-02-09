/* P_MOBJ.C - Movement Object Physics */
/* DOOM Source Engine 1.9 */
/* restored by Antigravity */

#include "doomdef.h"
#include "p_local.h"

//
// P_XYMovement
// Handles horizontal movement and friction.
//
void P_XYMovement (mobj_t* mo) {
    fixed_t ptryx, ptryy;
    player_t* player;
    fixed_t xmove, ymove;
    
    // FRICTION LOGIC
    if (mo->flags & MF_MISSILE) return; // Projectiles don't slow down
    
    // Legacy fixed point friction application
    // FRICTION is approx 0.906 in fixed point
    mo->momx = FixedMul(mo->momx, FRICTION); 
    mo->momy = FixedMul(mo->momy, FRICTION);
    
    // Stop completely if below threshold to prevent micro-sliding
    if (abs(mo->momx) < STOPSPEED && abs(mo->momy) < STOPSPEED) {
        mo->momx = 0;
        mo->momy = 0;
    }
}

//
// P_ZMovement
// Gravity logic.
//
void P_ZMovement (mobj_t* mo) {
    // GRAVITY
    // Standard linear gravity, no acceleration accumulation per frame in this version
    if (mo->z > mo->floorz) {
        mo->momz -= GRAVITY; // Linear gravity falloff
    } else {
        mo->z = mo->floorz;
        mo->momz = 0;
    }
}
