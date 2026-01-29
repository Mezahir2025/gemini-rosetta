/**
 * Modernized DOOM Sound Engine
 * Ported from s_sound.c (1993) to Web Audio API
 */

class DoomAudioEngine {
    constructor() {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        this.S_CLIPPING_DIST = 1200; // Original clipping distance
        this.S_CLOSE_DIST = 160;    // Max volume distance
        this.S_ATTENUATOR = (this.S_CLIPPING_DIST - this.S_CLOSE_DIST);
    }

    /**
     * Original DOOM distance approximation (from s_sound.c:771)
     * "Appox. eucledian distance fast"
     */
    approxDistance(dx, dy) {
        dx = Math.abs(dx);
        dy = Math.abs(dy);
        return (dx + dy - (Math.min(dx, dy) >> 1));
    }

    /**
     * Modern Stereo Panning using the legacy angle logic
     * @param {number} angleRad Angle from listener to source in radians
     */
    calculatePanning(angleRad, listenerAngleRad) {
        let relativeAngle = angleRad - listenerAngleRad;
        // In DOOM, sep = 128 - (fixed_sine[angle] * swing)
        // Here we return a value between -1 (Left) and 1 (Right)
        return Math.sin(relativeAngle);
    }

    /**
     * Legacy Volume Falloff logic (from s_sound.c:812)
     */
    calculateVolume(dist) {
        if (dist < this.S_CLOSE_DIST) return 1.0;
        if (dist > this.S_CLIPPING_DIST) return 0.0;

        let vol = (this.S_CLIPPING_DIST - dist) / this.S_ATTENUATOR;
        return Math.max(0, Math.min(1, vol));
    }

    /**
     * Play a sound with DOOM physics
     */
    playSound(sourceX, sourceY, listenerX, listenerY, listenerAngle) {
        let dx = sourceX - listenerX;
        let dy = sourceY - listenerY;
        let dist = this.approxDistance(dx, dy);
        
        let vol = this.calculateVolume(dist);
        let angleToSource = Math.atan2(dy, dx);
        let pan = this.calculatePanning(angleToSource, listenerAngle);

        console.log(`[AUDIO] Dist: ${dist.toFixed(2)}, Vol: ${vol.toFixed(2)}, Pan: ${pan.toFixed(2)}`);

        // Web Audio Implementation
        const oscillator = this.audioCtx.createOscillator();
        const gainNode = this.audioCtx.createGain();
        const panner = this.audioCtx.createStereoPanner();

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(220, this.audioCtx.currentTime); // 220Hz retro hum
        
        gainNode.gain.setValueAtTime(vol * 0.2, this.audioCtx.currentTime);
        panner.pan.setValueAtTime(pan, this.audioCtx.currentTime);

        oscillator.connect(panner).connect(gainNode).connect(this.audioCtx.destination);
        
        oscillator.start();
        oscillator.stop(this.audioCtx.currentTime + 0.1); // Short blip
    }
}
