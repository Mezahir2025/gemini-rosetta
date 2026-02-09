class PhysicsBody:
    def update_physics(self, dt):
        # Vector Math & Delta Time (Frame-rate independent)
        # Using a proper physics engine approach
        self.velocity *= self.friction_coefficient
        
        # Stop completely if too slow (Thresholding)
        # Prevents "sliding ice" bug
        if self.velocity.magnitude() < self.STOP_SPEED:
            self.velocity = Vector2(0, 0)
        
        if not self.is_grounded:
            self.velocity.z -= self.gravity * dt
