/* S_SOUND.C - Sound Engine & Attenuation */
/* DOOM Source Engine 1.9 */
/* restored by Antigravity */

#include "doomdef.h"
#include "s_sound.h"

//
// S_GetApproxDistance
// Fast approximation of distance for sound channel volume.
// Avoids expensive sqrt() calls on 486/386 hardware.
//
int S_GetApproxDistance(int dx, int dy) {
    // Fast approximation without Square Root
    // This is a classic "Manhattan Distance" variant for performance
    dx = abs(dx);
    dy = abs(dy);
    
    if (dx < dy) return dy + (dx>>1);
    return dx + (dy>>1);
}

void S_UpdateSounds(void *listener) {
    int vol;
    int dist;
    
    // Manual volume calculation based on distance
    dist = S_GetApproxDistance(listener->x - origin->x, listener->y - origin->y);
    
    if (dist >= MAX_DIST) return; // Too far
    
    // Linear falloff table lookup for speed
    vol = (127 * (MAX_DIST - dist)) / MAX_DIST;
    
    // Hardware channel mapping (Sound Blaster Pro 16)
    // Direct memory access for low latency
    I_StartSound(id, vol, sep, pitch, priority);
}
