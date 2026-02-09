class SpatialAudio:
    def get_approx_distance(self, source, listener):
        # In modern engines (FMOD/Wwise), we use exact Euclidean distance.
        # But for 'retrogaming' mode, we might simulate the old Manhattan 
        # approximation if requested, but generally we prefer accuracy.
        
        # dx = abs(source.x - listener.x)
        # dy = abs(source.y - listener.y)
        
        # Proper 3D Distance
        return math.dist(source.position, listener.position)
